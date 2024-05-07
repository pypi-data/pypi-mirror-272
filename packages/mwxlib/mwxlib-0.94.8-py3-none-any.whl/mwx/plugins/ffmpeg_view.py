#! python3
"""FFmpeg wrapper.
"""
from subprocess import Popen, PIPE
import numpy as np
import os
import wx
import wx.media

from mwx.graphman import Layer, Frame
from mwx.controls import LParam, Icon, Button, TextCtrl


def read_info(path):
    command = ['ffprobe',
               '-i', path,
               '-loglevel', 'quiet',    # no verbose
               '-print_format', 'json', # -format json
               '-show_streams',         # -streams info
               ]
    with Popen(command, stdout=PIPE, stderr=PIPE) as fp:
        ret, err = fp.communicate()
        if not err:
            return eval(ret)


def capture_video(path, ss=0):
    command = ['ffmpeg',
               '-ss', f"{ss}",          # Note: placing -ss before -i will be faster,
               '-i', path,              #       but maybe not accurate.
               '-frames:v', '1',        # -frame one shot
               '-f', 'rawvideo',        # -format raw
               '-pix_fmt', 'rgb24',     # rgb24, gray, etc.
               'pipe:'                  # pipe to stdout: '-'
               ]
    bufsize = 4096 # w * h * 3
    buf = b"" # bytearray()
    with Popen(command, stdout=PIPE) as fp:
        while 1:
            s = fp.stdout.read(bufsize)
            buf += s
            if len(s) < bufsize:
                break
    return np.frombuffer(buf, np.uint8)


def export_video(path, crop, ss, to, filename):
    command = ['ffmpeg',
               '-i', path,
               '-vf', f"{crop=}",
               '-ss', f"{ss}",
               '-to', f"{to}",
               '-y', filename,
               ]
    print('>', ' '.join(command))
    with Popen(command) as fp:
        ret, err = fp.communicate()


class MyFileDropLoader(wx.FileDropTarget):
    def __init__(self, target):
        wx.FileDropTarget.__init__(self)
        self.target = target
    
    def OnDropFiles(self, x, y, filenames):
        path = filenames[-1] # Only the last one will be loaded.
        if len(filenames) > 1:
            print("- Drop only one file please."
                  "Loading {!r} ...".format(path))
        self.target.load_media(path)
        return True


class Plugin(Layer):
    """Media loader using FFMpeg (installation required).
    """
    menukey = "Plugins/Extensions/FFMpeg viewer"
    ## menukey = "FFMpeg/"
    dockable = False
    
    def Init(self):
        self.mc = wx.media.MediaCtrl()
        self.mc.Create(self, size=(300,300),
                       style=wx.SIMPLE_BORDER,
                       szBackend=wx.media.MEDIABACKEND_WMP10
                       ## szBackend=wx.media.MEDIABACKEND_DIRECTSHOW
        )
        self.mc.ShowPlayerControls()
        self.mc.Bind(wx.media.EVT_MEDIA_LOADED, self.OnMediaLoaded)
        self.mc.Bind(wx.media.EVT_MEDIA_PAUSE, self.OnMediaPause)
        
        self.mc.SetDropTarget(MyFileDropLoader(self))
        
        self._path = None
        
        self.ss = LParam("ss:", # range/value will be set when loaded later.
                        handler=self.set_offset,
                        updater=self.get_offset,
                        )
        self.to = LParam("to:", # range/value will be set when loaded later.
                        handler=self.set_offset,
                        updater=self.get_offset,
                        )
        self.crop = TextCtrl(self, icon="cut", size=(130,-1),
                        handler=self.set_crop,
                        updater=self.get_crop,
                        )
        
        self.snp = Button(self, handler=self.snapshot, tip='Snapshot', icon='clock')
        self.exp = Button(self, handler=self.export, tip="Export", icon='save')
        
        self.rw = Button(self, handler=lambda v: self.seekdelta(-100), icon='|<-')
        self.fw = Button(self, handler=lambda v: self.seekdelta(+100), icon='->|')
        
        self.layout((self.mc,), expand=2)
        self.layout((self.ss, self.to, self.rw, self.fw,
                     self.snp, self.crop, self.exp),
                    expand=0, row=7, style='button', lw=12, cw=0, tw=64)
        
        self.menu[0:5] = [
            (1, "&Load file", Icon('open'),
                lambda v: self.load_media()),
                
            (2, "&Snapshot", Icon('clock'),
                lambda v: self.snapshot(),
                lambda v: v.Enable(self._path is not None)),
            (),
        ]
        
        self.parent.handler.bind("unknown_format", self.load_media)
    
    def Destroy(self):
        try:
            self.parent.handler.unbind("unknown_format", self.load_media)
            self.mc.Stop()
        finally:
            return Layer.Destroy(self)
    
    def OnMediaLoaded(self, evt):
        self.ss.range = (0, self.video_dur, 0.01)
        self.to.range = (0, self.video_dur, 0.01)
        self.Show()
        evt.Skip()
    
    def OnMediaPause(self, evt):
        evt.Skip()
    
    def load_media(self, path=None):
        if path is None:
            with wx.FileDialog(self, "Choose a media file",
                style=wx.FD_OPEN|wx.FD_CHANGE_DIR|wx.FD_FILE_MUST_EXIST) as dlg:
                if dlg.ShowModal() != wx.ID_OK:
                    return None
                path = dlg.Path
        self.mc.Load(path) # -> True (always)
        self.info = read_info(path)
        if self.info:
            v = next(x for x in self.info['streams'] if x['codec_type'] == 'video')
            ## self.video_fps = eval(v['r_frame_rate']) # real base frame rate
            self.video_fps = eval(v['avg_frame_rate'])  # averaged frame rate
            self.video_dur = eval(v['duration'])        # duration [s]
            w, h = v['width'], v['height']
            if v['tags'].get('rotate') in ('90', '270'):
                w, h = h, w  # transpose
            self.video_size = w, h
            self._path = path
            self.message(f"Loaded {path!r} successfully.")
            return True
        else:
            self.message(f"Failed to load file {path!r}.")
            return False
    
    DELTA = 1000 # correction ▲理由は不明 (WMP10 backend only?)
    
    def set_offset(self, tc):
        """Set offset value by referring to ss/to value."""
        try:
            self.mc.Seek(self.DELTA + int(tc.value * 1000))
        except Exception:
            pass
    
    def get_offset(self, tc):
        """Get offset value and assigns it to ss/to value."""
        try:
            tc.value = round(self.mc.Tell()) / 1000
        except Exception:
            pass
    
    def set_crop(self):
        """Set crop area (W:H:Left:Top) to roi."""
        frame = self.graph.frame
        if frame:
            try:
                w, h, xo, yo = eval(self.crop.Value.replace(':', ','))
                xo -= 0.5  # Correction with half-pixel
                yo -= 0.5  # to select left-top (not center) position
                nx = xo, xo+w
                ny = yo, yo+h
                frame.region = frame.xyfrompixel(nx, ny)
            except Exception:
                self.message("Failed to evaluate crop text.")
    
    def get_crop(self):
        """Get crop area (W:H:Left:Top) from roi."""
        crop = ''
        frame = self.graph.frame
        if frame:
            nx, ny = frame.xytopixel(*frame.region)
            if nx.size:
                xo, yo = nx[0], ny[1]
                xp, yp = nx[1], ny[0]
                crop = "{}:{}:{}:{}".format(xp-xo, yp-yo, xo, yo)
        if self._path and not crop:
            crop = "{}:{}:0:0".format(*self.video_size)
        self.crop.Value = crop
    
    def seekdelta(self, offset):
        """Seek relative position [ms]."""
        if wx.GetKeyState(wx.WXK_SHIFT):
            offset /= 10
        try:
            t = self.to.value + offset/1000
        except Exception as e:
            print(e)
        else:
            if self._path and 0 <= t < self.video_dur:
                self.to.value = round(t, 3)
            self.set_offset(self.to) # => seek
    
    def snapshot(self):
        """Create a snapshot of the current frame.
        Load the snapshot image into the graph window.
        """
        if not self._path:
            return
        t = self.mc.Tell()
        w, h = self.video_size
        buf = capture_video(self._path, t/1000).reshape((h,w,3))
        name = "{}-ss{}".format(os.path.basename(self._path), int(t))
        self.graph.load(buf, name)
    
    def export(self):
        """Export the cropped / clipped data to a media file."""
        if not self._path:
            return
        fout = "{}_clip".format(os.path.splitext(self._path)[0])
        with wx.FileDialog(self, "Save as",
                defaultFile=os.path.basename(fout),
                wildcard="Media file (*.mp4)|*.mp4|"
                         "Animiation (*.gif)|*.gif",
                style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return
            fout = dlg.Path
        export_video(self._path,
                     self.crop.Value or "{}:{}:0:0".format(*self.video_size),
                     self.ss.value, self.to.value, fout)
