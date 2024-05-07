#! python3
"""mwxlib param controller and wx custom controls.
"""
from itertools import chain
import wx
import wx.lib.platebtn as pb
import wx.lib.scrolledpanel as scrolled

from . import images
from .utilus import SSM
from .utilus import funcall as _F
from .framework import pack, Menu

import numpy as np
from numpy import nan, inf


def _Tip(*tips):
    """Concatenate tips with newline char."""
    return '\n'.join(filter(None, tips)).strip()


class Param(object):
    """Standard Parameter
    
    Args:
        name    : label
        range   : range
        value   : std_value (default is None)
        fmt     : text formatter or format:str (default is '%g')
                  `hex` specifies hexadecimal format
        handler : called when control changed
        updater : called when check changed
    
    Attributes:
        knobs       : knob list
        callback    : single state machine that handles following events
        
            - control -> when index changed by knobs or reset (handler)
            - update  -> when button pressed (updater)
            - check   -> when check marked (updater)
            - overflow -> when value overflows
            - underflow -> when value underflows
    """
    def __init__(self, name, range=None, value=None, fmt=None,
                 handler=None, updater=None, tip=None):
        self.knobs = []
        self.name = name
        self.range = range
        self.__std_value = value
        self.__value = value if value is not None else self.min
        self.__check = False
        if fmt is hex:
            self.__eval = lambda v: int(v, 16)
            self.__format = lambda v: '{:04X}'.format(int(v))
        else:
            self.__eval = lambda v: eval(v)
            self.__format = fmt or "{:,g}".format
            if isinstance(fmt, str): # support %-format:str (deprecated)
                self.__format = lambda v: fmt % v
        self.callback = SSM({
            'control' : [ _F(handler) ] if handler else [],
             'update' : [ _F(updater) ] if updater else [],
              'check' : [ _F(updater) ] if updater else [],
           'overflow' : [],
          'underflow' : [],
        })
        self._tooltip = _Tip(tip, handler.__doc__, updater.__doc__)
    
    def __str__(self, v=None):
        v = self.value if v is None else v
        try:
            return self.__format(v)
        except ValueError:
            return str(v)
    
    def __int__(self):
        return int(self.value)
    
    def __float__(self):
        return float(self.value)
    
    def __len__(self):
        return len(self.range)
    
    @wx.deprecatedMsg("Use `Param.callback.bind` instead.") #<DeprecationWarning>
    def bind(self, action=None, target='control'):
        return self.callback.bind(target, action)
    
    @wx.deprecatedMsg("Use `Param.callback.unbind` instead.") #<DeprecationWarning>
    def unbind(self, action=None, target='control'):
        return self.callback.unbind(target, action)
    
    def reset(self, v=None, backcall=True):
        """Reset value when indexed (by knobs) with callback."""
        if v is None or v == '':
            v = self.std_value
            if v is None:
                return
        elif v == 'nan': v = nan
        elif v == 'inf': v = inf
        elif isinstance(v, str):
            v = self.__eval(v.replace(',', '')) # eliminates commas
        self._set_value(v)
        if backcall:
            self.callback('control', self)
    
    def _set_value(self, v):
        """Set value and check the limit.
        If the value is out of range, modify the value.
        """
        if v is None:
            v = nan
        if v in (nan, inf):
            self.__value = v
            for knob in self.knobs:
                knob.update_ctrl(None, notify=False)
            return
        elif v == self.__value:
            return
        
        valid = (self.min <= v <= self.max)
        if valid:
            self.__value = v
        elif v < self.min:
            self.__value = self.min
            self.callback('underflow', self)
        else:
            self.__value = self.max
            self.callback('overflow', self)
        for knob in self.knobs:
            knob.update_ctrl(valid, notify=True)
    
    @property
    def check(self):
        """A knob check property (user defined)."""
        return self.__check
    
    @check.setter
    def check(self, v):
        self.__check = bool(v)
        self.callback('check', self)
        for knob in self.knobs:
            knob.update_label()
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, v):
        self.__name = v
        for knob in self.knobs:
            knob.update_label()
    
    @property
    def value(self):
        """Current value := std_value + offset."""
        return self.__value
    
    @value.setter
    def value(self, v):
        self._set_value(v)
    
    @property
    def std_value(self):
        """A standard value (default None)."""
        return self.__std_value
    
    @std_value.setter
    def std_value(self, v):
        self.__std_value = v
        for knob in self.knobs:
            knob.update_label()
    
    @property
    def offset(self):
        """Offset value
        If std_value is None, this is the same as value.
        """
        if self.std_value is not None:
            return self.value - self.std_value
        return self.value
    
    @offset.setter
    def offset(self, v):
        if self.std_value is not None:
            if v is not nan: # Note: nan +x is not nan
                v += self.std_value
        self._set_value(v)
    
    min = property(lambda self: self.__range[0])
    max = property(lambda self: self.__range[-1])
    
    @property
    def range(self):
        """Index range."""
        return self.__range
    
    @range.setter
    def range(self, v):
        if v is None:
            self.__range = [nan] # dummy data
        else:
            self.__range = sorted(v)
        for knob in self.knobs:
            knob.update_range() # list range of related knobs
    
    @property
    def index(self):
        """A knob index -> value."""
        return int(np.searchsorted(self.range, self.value))
    
    @index.setter
    def index(self, j):
        n = len(self)
        i = (0 if j<0 else j if j<n else -1)
        self._set_value(self.range[i])


class LParam(Param):
    """Linear Parameter
    
    Args:
        name    : label
        range   : range [min:max:step]
        value   : std_value (default is None)
        fmt     : text formatter or format:str (default is '%g')
                  `hex` specifies hexadecimal format
        handler : called when control changed
        updater : called when check changed
    
    Attributes:
        knobs       : knob list
        callback    : single state machine that handles following events
        
            - control -> when index changed by knobs or reset (handler)
            - check   -> when check ticks on/off (updater)
            - overflow -> when value overflows
            - underflow -> when value underflows
    """
    min = property(lambda self: self.__min)
    max = property(lambda self: self.__max)
    step = property(lambda self: self.__step)
    
    def __len__(self):
        return 1 + int(round((self.max - self.min) / self.step)) # includes [min,max]
    
    @property
    def range(self):
        """Index range."""
        return np.arange(self.min, self.max + self.step, self.step)
    
    @range.setter
    def range(self, v):
        if v is None:
            v = (0, 0)
        self.__min = v[0]
        self.__max = v[1]
        self.__step = v[2] if len(v) > 2 else 1
        for knob in self.knobs:
            knob.update_range() # linear range of related knobs
    
    @property
    def index(self):
        """A knob index -> value
        Returns -1 if the value is nan or inf.
        """
        if self.value in (nan, inf):
            return -1
        return int(round((self.value - self.min) / self.step))
    
    @index.setter
    def index(self, j):
        return self._set_value(self.min + j * self.step)


## --------------------------------
## Knob unit for Parameter Control 
## --------------------------------

class Knob(wx.Panel):
    """Parameter controller unit
    
    In addition to direct key input to the textctrl,
    [up][down][wheelup][wheeldown] keys can be used,
    with modifiers S- 2x, C- 16x, and M- 256x steps.
    [Mbutton] resets to the std. value if it exists.
    
    Args:
        param   : <Param> or <LParam> object
        type    : ctrl type (slider[*], [hv]spin, choice, None)
        style   : style of label
                  None -> static text (default)
                  chkbox -> label with check box
                  button -> label with flat button
        editable: textctrl is editable or readonly
        cw      : width of ctrl
        lw      : width of label
        tw      : width of textbox
        h       : height of widget (defaults to 22)
    """
    @property
    def param(self):
        """Param object referred from knobs."""
        return self.__par
    
    @param.setter
    def param(self, v):
        self.__par.knobs.remove(self)
        self.__par = v
        self.__par.knobs.append(self)
        self.update_range()
        self.update_ctrl()
    
    def __init__(self, parent, param, type=None,
                 style=None, editable=1, cw=-1, lw=-1, tw=-1, h=22,
                 **kwargs):
        wx.Panel.__init__(self, parent, **kwargs)
        
        assert isinstance(param, Param),\
          "Argument `param` must be an instance of Param class."
        
        self.__bit = 1
        self.__par = param
        self.__par.knobs.append(self) # パラメータの関連付けを行う
        
        if type is None:
            type = 'slider'
            cw = 0
        elif type == 'choice':
            if cw < 0:
                cw = 20
            cw += tw
            tw = 0
        
        label = self.__par.name + '  '
        
        if style == 'chkbox':
            if lw >= 0:
                lw += 16
            self.label = wx.CheckBox(self, label=label, size=(lw,-1))
            self.label.Bind(wx.EVT_CHECKBOX, self.OnCheck)
            
        elif style == 'button':
            if lw >= 0:
                lw += 16
            self.label = pb.PlateButton(self, label=label, size=(lw,-1),
                            style=pb.PB_STYLE_DEFAULT|pb.PB_STYLE_SQUARE)
            self.label.Bind(wx.EVT_BUTTON, self.OnPress)
            
        elif not style:
            self.label = wx.StaticText(self, label=label, size=(lw,-1))
        else:
            raise Exception("unknown style: {!r}".format(style))
        
        self.label.Enable(lw)
        self.label.Bind(wx.EVT_MIDDLE_DOWN, lambda v: self.__par.reset())
        
        self.label.SetToolTip(self.__par._tooltip)
        
        if editable:
            self.text = wx.TextCtrl(self, size=(tw,h), style=wx.TE_PROCESS_ENTER)
            self.text.Bind(wx.EVT_TEXT_ENTER, self.OnTextEnter)
            self.text.Bind(wx.EVT_KILL_FOCUS, self.OnTextExit)
            self.text.Bind(wx.EVT_KEY_DOWN, self.OnTextKeyDown)
            self.text.Bind(wx.EVT_KEY_UP, self.OnTextKeyUp)
            self.text.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
            self.text.Bind(wx.EVT_MIDDLE_DOWN, lambda v: self.__par.reset())
        else:
            self.text = wx.TextCtrl(self, size=(tw,h), style=wx.TE_READONLY)
        
        self.text.Enable(tw)
        
        if type == 'slider':
            self.ctrl = wx.Slider(self, size=(cw,h), style=wx.SL_HORIZONTAL)
            self.ctrl.Bind(wx.EVT_SCROLL_CHANGED, self.OnScroll)
            self.ctrl.Bind(wx.EVT_KEY_DOWN, self.OnCtrlKeyDown)
            self.ctrl.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
            
        elif type == 'slider*':
            self.ctrl = wx.Slider(self, size=(cw,h), style=wx.SL_HORIZONTAL)
            self.ctrl.Bind(wx.EVT_SCROLL, self.OnScroll) # called while dragging
            self.ctrl.Bind(wx.EVT_SCROLL_CHANGED, lambda v: None) # pass no action
            self.ctrl.Bind(wx.EVT_KEY_DOWN, self.OnCtrlKeyDown)
            self.ctrl.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
            
        elif type == 'spin' or type =='hspin':
            self.ctrl = wx.SpinButton(self, size=(cw,h), style=wx.SP_HORIZONTAL)
            self.ctrl.Bind(wx.EVT_SPIN, self.OnScroll)
            self.ctrl.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
            
        elif type == 'vspin':
            self.ctrl = wx.SpinButton(self, size=(cw,h), style=wx.SP_VERTICAL)
            self.ctrl.Bind(wx.EVT_SPIN, self.OnScroll)
            self.ctrl.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
            
        elif type == 'choice':
            self.ctrl = wx.Choice(self, size=(cw,h))
            self.ctrl.Bind(wx.EVT_CHOICE, self.OnScroll)
            self.ctrl.SetValue = self.ctrl.SetSelection # setter of choice
            self.ctrl.GetValue = self.ctrl.GetSelection # getter (ditto)
            
        else:
            raise Exception("unknown type: {!r}".format(type))
        
        self.ctrl.Enable(cw != 0)
        self.ctrl.Bind(wx.EVT_MIDDLE_DOWN, lambda v: self.__par.reset())
        
        c = (cw and type != 'vspin')
        self.SetSizer(
            pack(self, (
                (self.label, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, lw and 1),
                (self.text,  0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, tw and 1),
                (self.ctrl,  c, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, cw and 1),
            ))
        )
        self.update_range()
        self.update_ctrl()
        
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)
    
    def OnDestroy(self, evt):
        self.__par.knobs.remove(self) # パラメータの関連付けを解除する
        evt.Skip()
    
    def update_range(self):
        v = self.__par
        if isinstance(self.ctrl, wx.Choice): #<wx.Choice>
            items = [v.__str__(x) for x in v.range]
            if items != self.ctrl.Items:
                self.ctrl.SetItems(items)
                self.ctrl.SetStringSelection(str(v))
        else:
            self.ctrl.SetRange(0, len(v)-1) #<wx.Slider> <wx.SpinButton>
    
    def update_label(self):
        v = self.__par
        if isinstance(self.label, wx.CheckBox):
            self.label.SetValue(v.check)
        
        if self.label.IsEnabled():
            t = '  ' if v.std_value is None or v.value == v.std_value else '*'
            self.label.SetLabel(v.name + t)
            self.label.Refresh()
    
    def update_ctrl(self, valid=True, notify=False):
        v = self.__par
        try:
            j = v.index
        except (OverflowError, ValueError):
            ## OverflowError: cannot convert float infinity to integer
            ## ValueError: cannot convert float NaN to integer
            j = -1
        
        self.ctrl.SetValue(j)
        self.text.SetValue(str(v))
        if valid:
            if notify:
                if self.text.BackgroundColour != '#ffff80':
                    wx.CallAfter(wx.CallLater, 1000,
                        self.set_textcolour, '#ffffff')
                    self.set_textcolour('#ffff80') # light-yellow
                else:
                    self.set_textcolour('#ffffff') # True: white
            else:
                self.set_textcolour('#ffffff') # True: white
        elif valid is None:
            self.set_textcolour('#ffff80') # None: light-yellow
        else:
            self.set_textcolour('#ff8080') # False: light-red
        self.update_label()
    
    def set_textcolour(self, c):
        if self:
            if self.text.IsEditable():
                self.text.BackgroundColour = c
            self.text.Refresh()
    
    def shift(self, evt, bit):
        if bit:
            if evt.ShiftDown():   bit *= 2
            if evt.ControlDown(): bit *= 16
            if evt.AltDown():     bit *= 256
        v = self.__par
        j = self.ctrl.GetValue() + bit
        if j != v.index:
            v.index = j
            v.reset(v.value)
    
    def OnScroll(self, evt): #<wx._core.ScrollEvent><wx._controls.SpinEvent><wx._core.CommandEvent>
        v = self.__par
        j = self.ctrl.GetValue()
        if j != v.index:
            v.index = j
            v.reset(v.value)
        evt.Skip()
    
    def OnMouseWheel(self, evt): #<wx._core.MouseEvent>
        self.shift(evt, 1 if evt.WheelRotation>0 else -1)
        evt.Skip(False)
    
    def OnCtrlKeyDown(self, evt): #<wx._core.KeyEvent>
        key = evt.GetKeyCode()
        if key == wx.WXK_LEFT: return self.shift(evt, -1)
        if key == wx.WXK_RIGHT: return self.shift(evt, 1)
        
        def focus(c):
            if isinstance(c, Knob) and c.ctrl.IsEnabled():
                c.ctrl.SetFocus()
                return True
        
        ls = next(x for x in self.Parent.layout_groups if self in x)
        i = ls.index(self)
        if key == wx.WXK_DOWN: return any(focus(c) for c in ls[i+1:])
        if key == wx.WXK_UP: return any(focus(c) for c in ls[i-1::-1])
    
    def OnTextKeyUp(self, evt): #<wx._core.KeyEvent>
        evt.Skip()
    
    def OnTextKeyDown(self, evt): #<wx._core.KeyEvent>
        key = evt.GetKeyCode()
        if key == wx.WXK_DOWN: return self.shift(evt, -1)
        if key == wx.WXK_UP: return self.shift(evt, 1)
        if key == wx.WXK_ESCAPE:
            self.__par.reset(self.__par.value, backcall=None) # restore value
        evt.Skip()
    
    def OnTextEnter(self, evt): #<wx._core.CommandEvent>
        evt.Skip()
        x = self.text.Value.strip()
        self.__par.reset(x)
    
    def OnTextExit(self, evt): #<wx._core.FocusEvent>
        x = self.text.Value.strip()
        if x != str(self.__par):
            try:
                self.__par.reset(x) # reset value if focus out
            except Exception:
                self.text.SetValue(str(self.__par))
                self.__par.reset(self.__par.value, backcall=None) # restore value
        evt.Skip()
    
    def OnCheck(self, evt): #<wx._core.CommandEvent>
        self.__par.check = evt.IsChecked()
        evt.Skip()
    
    def OnPress(self, evt): #<wx._core.CommandEvent>
        self.__par.callback('update', self.__par)
        evt.Skip()
    
    def Enable(self, p=True):
        self.label.Enable(p)
        self.ctrl.Enable(p)
        self.text.Enable(p)


class ControlPanel(scrolled.ScrolledPanel):
    """Scrollable Control Panel
    """
    def __init__(self, *args, **kwargs):
        scrolled.ScrolledPanel.__init__(self, *args, **kwargs)
        
        self.SetSizer(pack(self, [], orient=wx.VERTICAL))
        self.SetupScrolling()
        
        self.__groups = []
        self.__params = []
        
        self.menu = [
            (wx.ID_COPY, "&Copy params", "Copy params",
                lambda v: self.copy_to_clipboard(checked_only=wx.GetKeyState(wx.WXK_SHIFT)),
                lambda v: v.Enable(self.__params != [])),
                
            (wx.ID_PASTE, "&Paste params", "Read params",
                lambda v: self.paste_from_clipboard(checked_only=wx.GetKeyState(wx.WXK_SHIFT)),
                lambda v: v.Enable(self.__params != [])),
            (),
            (wx.ID_RESET, "&Reset params", "Reset params",
                lambda v: self.set_params(checked_only=wx.GetKeyState(wx.WXK_SHIFT)),
                lambda v: v.Enable(self.__params != [])),
        ]
        self.Bind(wx.EVT_CONTEXT_MENU,
                  lambda v: Menu.Popup(self, self.menu))
        
        self.Bind(wx.EVT_LEFT_DOWN, self.OnToggleFold)
        
        self.Bind(wx.EVT_SCROLLWIN_THUMBRELEASE, self.OnRecalcLayout)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnRecalcLayout)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnRecalcLayout)
    
    def OnRecalcLayout(self, evt): #<wx._core.ScrollWinEvent>
        self.Layout()
        evt.Skip()
    
    def OnToggleFold(self, evt): #<wx._core.MouseEvent>
        x, y = evt.Position
        for child in self.Sizer.Children: # child <wx._core.SizerItem>
            if child.IsShown():
                obj = child.Sizer or child.Window
                if isinstance(obj, (wx.StaticBoxSizer, wx.StaticBox)):
                    cx, cy = obj.Position
                    if cx < x < cx + obj.Size[0] and cy < y < cy+22:
                        for cc in obj.Children: # child of child <wx._core.SizerItem>
                            cc.Show(not cc.IsShown())
                        self.Layout()
                        self.SendSizeEvent()
                        break
        evt.Skip()
    
    ## --------------------------------
    ## Layout commands and attributes
    ## --------------------------------
    @property
    def layout_groups(self):
        return self.__groups
    
    def is_enabled(self, groupid, pred=all):
        return pred(win.Enabled for win in self.__groups[groupid])
    
    def enable(self, groupid, p=True):
        for win in self.__groups[groupid]: # child could be deep nesting
            win.Enable(p)
    
    def is_shown(self, groupid):
        ## child = self.Sizer.Children[groupid]
        ## return child.IsShown()
        return self.Sizer.IsShown(groupid % len(self.__groups))
    
    def show(self, groupid, p=True):
        """Show/hide all including the box."""
        ## child = self.Sizer.Children[groupid]
        ## child.Show(p)
        self.Sizer.Show(groupid % len(self.__groups), p)
        ## self.Sizer.Fit(self) # do Fit(self.Parent) if needed
        self.Layout()
        self.Parent.SendSizeEvent() # let parent redraw the child panel
    
    def is_folded(self, groupid):
        child = self.Sizer.Children[groupid]
        return not any(cc.IsShown() for cc in child.Sizer.Children)
    
    def fold(self, groupid, p=True):
        """Fold/unfold the boxed group."""
        child = self.Sizer.Children[groupid]
        if isinstance(child.Sizer, wx.StaticBoxSizer) and child.IsShown():
            for cc in child.Sizer.Children: # child of child <wx._core.SizerItem>
                cc.Show(not p)
            ## self.Sizer.Fit(self) # do Fit(self.Parent) if needed
            self.Layout()
            self.Parent.SendSizeEvent() # let parent redraw the child panel
    
    def layout(self, items, title=None,
               row=0, expand=0, border=2, hspacing=1, vspacing=1,
               show=True, visible=True, align=wx.ALIGN_LEFT, **kwargs):
        """Do layout (cf. Layout).
        
        Args:
            items   : list of Params, wx.Objects, tuple of sizing, or None
            title   : box header string (default is None - no box)
            row     : number of row to arange widgets
            expand  : (0) fixed size
                      (1) to expand horizontally
                      (2) to expand horizontally and vertically
            border  : size of outline border
            hspacing: horizontal spacing among packed objs inside the group
            vspacing: vertical spacing among packed objs inside the group
            show    : fold or unfold the boxed group
            visible : Hide the boxed group if False
            align   : alignment flag (wx.ALIGN_*) default is ALIGN_LEFT
            **kwargs: extra keyword arguments given for Knob
        """
        objs = [Knob(self, c, **kwargs) if isinstance(c, Param)
                else c for c in items]
        
        p = wx.EXPAND if expand > 0 else wx.ALIGN_CENTER
        if row > 0:
            oblist = [pack(self, objs[i:i+row], orient=wx.HORIZONTAL,
                           style=(expand>0, p | wx.LEFT | wx.RIGHT, hspacing))
                           for i in range(0, len(objs), row)]
        else:
            oblist = objs
        
        p = wx.EXPAND if expand > 0 else align
        sizer = pack(self, oblist, label=title, orient=wx.VERTICAL,
                     style=(expand>1, p | wx.BOTTOM | wx.TOP, vspacing))
        
        self.Sizer.Add(sizer, expand>1, p | wx.ALL, border)
        
        ## Register object and parameter groups
        def flatiter(a):
            for c in a:
                if isinstance(c, tuple):
                    yield from flatiter(c)
                elif isinstance(c, wx.Object):
                    yield c
        self.__groups.append(list(flatiter(objs)))
        
        def variter(a):
            for c in a:
                if isinstance(c, Knob):
                    yield c.param
                elif hasattr(c, 'value'):
                    yield c
        self.__params.append(list(variter(objs)))
        
        ## Set appearance of the layout group
        self.show(-1, visible)
        self.fold(-1, not show)
        self.Sizer.Fit(self)
    
    ## --------------------------------
    ## 外部入出力／クリップボード通信
    ## --------------------------------
    @property
    def parameters(self):
        return [p.value for p in self.get_params()]
    
    @parameters.setter
    def parameters(self, v):
        self.set_params(v)
    
    def get_params(self, checked_only=False):
        params = chain(*self.__params)
        if not checked_only:
            return params
        return filter(lambda c: getattr(c, 'check', None), params)
    
    def set_params(self, argv=None, checked_only=False):
        params = self.get_params(checked_only)
        if argv is None:
            for p in params:
                try:
                    p.reset()
                except (AttributeError, TypeError):
                    pass
        else:
            for p, v in zip(params, argv):
                try:
                    p.reset(v) # eval v:str -> value
                except AttributeError:
                    p.value = v
                except Exception as e: # failed to eval
                    print(f"- Failed to reset {p!r}:", e)
                    pass
    
    reset_params = set_params #: for backward compatibility
    
    def copy_to_clipboard(self, checked_only=False):
        params = self.get_params(checked_only)
        text = '\t'.join(str(p) if isinstance(p, Param) else
                         str(p.value) for p in params)
        Clipboard.write(text)
    
    def paste_from_clipboard(self, checked_only=False):
        text = Clipboard.read()
        if text:
            self.set_params(text.split('\t'), checked_only)


class Clipboard:
    """Clipboard interface of text and image
    
    This does not work unless wx.App instance exists.
    The clipboard data cannot be transferred unless wx.Frame exists.
    """
    @staticmethod
    def read(verbose=True):
        do = wx.TextDataObject()
        if wx.TheClipboard.Open():
            wx.TheClipboard.GetData(do)
            wx.TheClipboard.Close()
            text = do.GetText()
            if verbose:
                print("From clipboard: {}".format(text))
            return text
        else:
            print("- Unable to open clipboard.")
    
    @staticmethod
    def write(text, verbose=True):
        do = wx.TextDataObject(str(text))
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(do)
            wx.TheClipboard.Flush()
            wx.TheClipboard.Close()
            if verbose:
                print("To clipboard: {}".format(text))
        else:
            print("- Unable to open clipboard.")
    
    @staticmethod
    def imread(verbose=True):
        do = wx.BitmapDataObject()
        if wx.TheClipboard.Open():
            wx.TheClipboard.GetData(do)
            wx.TheClipboard.Close()
            bmp = do.GetBitmap()
        else:
            print("- Unable to open clipboard.")
            return
        try:
            ## Convert bmp --> buf
            img = bmp.ConvertToImage()
            buf = np.array(img.GetDataBuffer()) # do copy, don't ref
            if verbose:
                print("From clipboard {:.1f} Mb data".format(buf.nbytes/1e6))
            w, h = img.GetSize()
            return buf.reshape(h, w, 3)
        except Exception:
            print("- The contents of the clipboard are not images.")
    
    @staticmethod
    def imwrite(buf, verbose=True):
        try:
            ## Convert buf --> bmp
            h, w = buf.shape[:2]
            if buf.ndim < 3:
                ## buf = np.array([buf] * 3).transpose((1,2,0)) # convert to gray bitmap
                buf = buf.repeat(3, axis=1) # convert to gray bitmap
            img = wx.Image(w, h, buf.tobytes())
            bmp = img.ConvertToBitmap()
        except Exception:
            print("- The contents of the clipboard are not images.")
            return
        do = wx.BitmapDataObject(bmp)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(do)
            wx.TheClipboard.Flush()
            wx.TheClipboard.Close()
            if verbose:
                print("To clipboard: {:.1f} Mb data".format(buf.nbytes/1e6))
        else:
            print("- Unable to open clipboard.")


## --------------------------------
## Wx custom controls and bitmaps 
## --------------------------------
if 1:
    _provided_arts = {
            'cut' : wx.ART_CUT,
           'copy' : wx.ART_COPY,
          'paste' : wx.ART_PASTE,
         'delete' : wx.ART_DELETE,
           'book' : wx.ART_HELP_BOOK,
           'page' : wx.ART_HELP_PAGE,
            'exe' : wx.ART_EXECUTABLE_FILE,
           'file' : wx.ART_NORMAL_FILE,
       'file_new' : wx.ART_NEW,
   'file_missing' : wx.ART_MISSING_IMAGE,
           'find' : wx.ART_FIND,
         'folder' : wx.ART_FOLDER,
           'open' : wx.ART_FILE_OPEN,
           'save' : wx.ART_FILE_SAVE,
         'saveas' : wx.ART_FILE_SAVE_AS,
              '?' : wx.ART_QUESTION,
              '!' : wx.ART_INFORMATION,
             '!!' : wx.ART_WARNING,
            '!!!' : wx.ART_ERROR,
              '+' : wx.ART_PLUS,
              '-' : wx.ART_MINUS,
              'x' : wx.ART_DELETE,
              't' : wx.ART_TICK_MARK,
              '~' : wx.ART_GO_HOME,
           'undo' : wx.ART_UNDO,
           'redo' : wx.ART_REDO,
             'up' : wx.ART_GO_UP,
             'dn' : wx.ART_GO_DOWN,
             '<-' : wx.ART_GO_BACK,
             '->' : wx.ART_GO_FORWARD,
            '|<-' : wx.ART_GOTO_FIRST,
            '->|' : wx.ART_GOTO_LAST,
    }
    _custom_images = {
        k:v for k, v in vars(images).items()
            if isinstance(v, wx.lib.embeddedimage.PyEmbeddedImage)
    }

def Icon(key, size=None):
    """Returns an iconic bitmap with the specified size (w,h).
    
    The key is either Icon.provided_arts or Icon.custom_images key.
    If the key is empty it returns a transparent bitmap, otherwise NullBitmap.
    """
    if key:
        try:
            art = _custom_images.get(key) # None => AttributeError
            if not size:
                bmp = art.GetBitmap()
            else:
                bmp = (art.GetImage()
                          .Scale(*size, wx.IMAGE_QUALITY_NEAREST)
                          .ConvertToBitmap())
        except Exception:
            art = _provided_arts.get(key) or key
            bmp = wx.ArtProvider.GetBitmap(art, wx.ART_OTHER, size or (16,16))
        return bmp
    
    ## Note: null (0-shaped) bitmap fails with AssertionError from 4.1.1
    if key == '':
        bmp = wx.Bitmap(size or (16,16))
        if 1:
            dc = wx.MemoryDC(bmp)
            dc.SetBackground(wx.Brush('black'))
            dc.Clear()
            del dc
        bmp.SetMaskColour('black') # return dummy-sized blank bitmap
        return bmp
    
    return wx.NullBitmap # The standard wx controls accept this,

Icon.provided_arts = _provided_arts
Icon.custom_images = _custom_images


def Icon2(back, fore, size=None, subsize=0.6):
    if not size:
        size = (16,16)
    if isinstance(subsize, float):
        subsize = wx.Size(size) * subsize
    back = Icon(back, size)
    fore = Icon(fore, subsize)
    x = size[0] - subsize[0]
    y = size[1] - subsize[1]
    dc = wx.MemoryDC(back)
    dc.DrawBitmap(fore, x, y, useMask=True)
    del dc
    return back


def Iconify(icon, w, h):
    ## if wx.VERSION >= (4,1,0):
    try:
        import wx.svg
        import requests
        url = "https://api.iconify.design/{}.svg".format(icon.replace(':', '/'))
        res = requests.get(url, timeout=3.0)
        img = wx.svg.SVGimage.CreateFromBytes(res.content)
        bmp = img.ConvertToScaledBitmap(wx.Size(w, h))
        return bmp
    except Exception:
        print("- Failed to load iconify.design/{}".format(icon))
        pass


def _Icon(v):
    if isinstance(v, (str, bytes)):
        return Icon(v)
    if isinstance(v, wx.lib.embeddedimage.PyEmbeddedImage):
        return v.GetBitmap()
    return v


class Button(pb.PlateButton):
    """Flat button
    
    Args:
        label   : button label
        handler : event handler when the button is pressed
        icon    : key:str or bitmap for button icon
        **kwargs: keywords for wx.lib.platebtn.PlateButton
    """
    @property
    def icon(self):
        """Icon key:str or bitmap."""
        return self.__icon
    
    @icon.setter
    def icon(self, v):
        self.__icon = v
        self.SetBitmap(_Icon(v))
        self.Refresh()
    
    def __init__(self, parent, label='',
                 handler=None, icon=None, tip='', **kwargs):
        kwargs.setdefault('style', pb.PB_STYLE_DEFAULT | pb.PB_STYLE_SQUARE)
        pb.PlateButton.__init__(self, parent, -1, label, **kwargs)
        
        if handler:
            self.Bind(wx.EVT_BUTTON, _F(handler))
        
        self.ToolTip = _Tip(tip, handler.__doc__)
        self.icon = icon
    
    def SetBitmap(self, bmp):
        """Set the bitmap displayed in the button.
        (override) If it fails, it clears the bitmap.
        """
        try:
            pb.PlateButton.SetBitmap(self, bmp)
        except Exception:
            self._bmp = dict(enable=None, disable=None)


class ToggleButton(wx.ToggleButton):
    """Togglable button
    
    Args:
        label   : button label
        handler : event handler when the button is pressed
        icon    : key:str or bitmap for button icon
        **kwargs: keywords for wx.ToggleButton
    
    Note:
        To get the status, check Value or event.GetInt or event.IsChecked.
    """
    @property
    def icon(self):
        """Icon key:str or bitmap."""
        return self.__icon
    
    @icon.setter
    def icon(self, v):
        self.__icon = v
        if isinstance(v, tuple):
            self.SetBitmap(_Icon(v[0]))
            self.SetBitmapPressed(_Icon(v[1]))
        elif v:
            self.SetBitmap(_Icon(v))
        self.Refresh()
    
    def __init__(self, parent, label='',
                 handler=None, icon=None, tip='', **kwargs):
        wx.ToggleButton.__init__(self, parent, -1, label, **kwargs)
        
        if handler:
            self.Bind(wx.EVT_TOGGLEBUTTON, _F(handler))
        
        self.ToolTip = _Tip(tip, handler.__doc__)
        self.icon = icon


class TextCtrl(wx.Control):
    """Text panel
    
    Args:
        label   : button label
        handler : event handler when text is entered
        updater : event handler when the button is pressed
        icon    : key:str or bitmap for button icon
        readonly: flag:bool (equiv. style=wx.TE_READONLY)
        **kwargs: keywords for wx.TextCtrl
                  e.g., value:str
    """
    Value = property(
        lambda self: self._ctrl.GetValue(),
        lambda self,v: self._ctrl.SetValue(v),
        doc="textctrl value:str")
    
    value = Value #: internal use only
    
    @property
    def icon(self):
        """Icon key:str or bitmap."""
        return self._btn.icon
    
    @icon.setter
    def icon(self, v):
        self._btn.icon = v
    
    def __init__(self, parent, label='',
                 handler=None, updater=None, size=(-1,-1),
                 icon=None, tip='', readonly=False, **kwargs):
        wx.Control.__init__(self, parent, size=size, style=wx.BORDER_NONE)
        
        kwargs['style'] = (kwargs.get('style', 0)
                            | wx.TE_PROCESS_ENTER
                            | (wx.TE_READONLY if readonly else 0))
        
        tooltip = _Tip(tip, handler.__doc__, updater.__doc__)
        
        self._ctrl = wx.TextCtrl(self, **kwargs)
        self._btn = Button(self, label, None, icon, tooltip,
                           size=(-1,-1) if label or icon else (0,0))
        self.SetSizer(
            pack(self, (
                (self._btn, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 0),
                (self._ctrl, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 0),
            ))
        )
        if handler:
            self._handler = _F(handler)
            self._ctrl.Bind(wx.EVT_TEXT_ENTER, lambda v: self._handler(self))
        if updater:
            self._updater = _F(updater)
            self._btn.Bind(wx.EVT_BUTTON, lambda v: self._updater(self))
    
    def reset(self, v):
        try:
            self.Value = v
            self._handler(self)
        except AttributeError:
            pass


class Choice(wx.Control):
    """Editable Choice (ComboBox) panel
    
    Args:
        label   : button label
        handler : event handler when text is entered or item is selected
        updater : event handler when the button is pressed
        icon    : key:str or bitmap for button icon
        readonly: flag:bool (equiv. style=wx.CB_READONLY)
        **kwargs: keywords for wx.ComboBox
                  e.g., choices:list
    
    Note:
        If the input item is not found in the choices,
        it will be added to the list (unless readonly)
    """
    Value = property(
        lambda self: self._ctrl.GetValue(),
        lambda self,v: self._ctrl.SetValue(v),
        doc="combobox value:str")
    
    value = Value #: internal use only
    
    Selection = property(
        lambda self: self._ctrl.GetSelection(),
        lambda self,v: self._ctrl.SetSelection(v), # int or NOT_FOUND(-1)
        doc="combobox selection:int")
    
    Items = property(
        lambda self: self._ctrl.GetItems(),
        lambda self,v: self._ctrl.SetItems(v),
        doc="combobox items:list")
    
    @property
    def icon(self):
        """Icon key:str or bitmap."""
        return self._btn.icon
    
    @icon.setter
    def icon(self, v):
        self._btn.icon = v
    
    def __init__(self, parent, label='',
                 handler=None, updater=None, size=(-1,-1),
                 icon=None, tip='', readonly=False, **kwargs):
        wx.Control.__init__(self, parent, size=size, style=wx.BORDER_NONE)
        
        kwargs['style'] = (kwargs.get('style', 0)
                            | wx.TE_PROCESS_ENTER
                            | (wx.CB_READONLY if readonly else 0))
        
        tooltip = _Tip(tip, handler.__doc__, updater.__doc__)
        
        self._ctrl = wx.ComboBox(self, **kwargs)
        self._btn = Button(self, label, None, icon, tooltip,
                           size=(-1,-1) if label or icon else (0,0))
        self.SetSizer(
            pack(self, (
                (self._btn, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 0),
                (self._ctrl, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 0),
            ))
        )
        if handler:
            self._handler = _F(handler)
            self._ctrl.Bind(wx.EVT_TEXT_ENTER, lambda v: self._handler(self))
            self._ctrl.Bind(wx.EVT_COMBOBOX, lambda v: self._handler(self))
        self._ctrl.Bind(wx.EVT_TEXT_ENTER, self.OnTextEnter)
        if updater:
            self._updater = _F(updater)
            self._btn.Bind(wx.EVT_BUTTON, lambda v: self._updater(self))
    
    def reset(self, v):
        try:
            self.Value = v
            self._handler(self)
        except AttributeError:
            pass
    
    def OnTextEnter(self, evt):
        s = evt.String.strip()
        if not s:
            self._ctrl.SetSelection(-1)
        elif s not in self._ctrl.Items:
            self._ctrl.Append(s)
            self._ctrl.SetStringSelection(s)
        evt.Skip()


class Indicator(wx.Control):
    """Traffic light indicator
    
    Args:
        colors  : list of colors (default is tricolour) cf. wx.ColourDatabase
        value   : initial value
        **kwargs: keywords for wx.Control
    """
    @property
    def Value(self):
        return self.__value
    
    @Value.setter
    def Value(self, v):
        self.__value = int(v)
        self.Refresh()
    
    def update_design(self, **kwargs):
        """Update design attributes.
        
        This method is useful for changing colors, spacing, radius, etc.
        The best size will be automatically invalidated and re-calculated.
        
        Args:
            **kwargs: class attributes, e.g. colors, spacing, radius.
        
        Note:
            This method has no effect on properties such as Value.
        """
        self.__dict__.update(kwargs)
        self.InvalidateBestSize()
    
    colors = ('green', 'yellow', 'red') # default tricolor style
    backgroundColour = 'dark gray'
    foregroundColour = 'light gray'
    spacing = 7
    radius = 4
    glow = 0
    
    def __init__(self, parent, colors=None, value=0,
                 style=wx.BORDER_NONE, **kwargs):
        wx.Control.__init__(self, parent, style=style, **kwargs)
        
        self.__value = value
        if colors is not None:
            self.colors = colors
        
        ## Sizes the window to fit its best size.
        ## May be needed if sizer is not defined.
        self.InvalidateBestSize()
        self.Fit()
        
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT) # to avoid flickering
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
    
    def DoGetBestSize(self):
        N = len(self.colors)
        s = self.spacing
        return wx.Size((2*s-1)*N+3, 2*s+2)
    
    def OnSize(self, evt):
        self.Refresh()
    
    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.Clear()
        N = len(self.colors)
        r = self.radius
        s = self.spacing
        ss = 2*s-1
        w, h = self.ClientSize
        
        dc.SetPen(wx.Pen(self.backgroundColour, style=wx.PENSTYLE_SOLID))
        if self.backgroundColour:
            dc.SetBrush(wx.Brush(self.backgroundColour, style=wx.BRUSHSTYLE_SOLID))
        else:
            dc.SetBrush(wx.Brush(self.backgroundColour, style=wx.BRUSHSTYLE_TRANSPARENT))
        dc.DrawRoundedRectangle(0, h//2-s, ss*N+1, 2*s, s)
        
        if self.glow:
            gc = wx.GraphicsContext.Create(dc)
            gc.SetPen(gc.CreatePen(wx.TRANSPARENT_PEN))
            path = gc.CreatePath()
            stops = wx.GraphicsGradientStops()
            stops.Add(wx.GraphicsGradientStop(wx.Colour(255,255,255,128), r/s))
            stops.Add(wx.GraphicsGradientStop(wx.TransparentColour, 1.0))
        
        dc.SetPen(wx.Pen(self.foregroundColour, style=wx.PENSTYLE_TRANSPARENT))
        for j, name in enumerate(self.colors):
            b = self.__value & (1 << j)
            x = ss*(N-1-j)+s
            y = h//2
            if b and self.glow:
                gc.SetBrush(gc.CreateRadialGradientBrush(x, y, x, y, s, stops))
                path.AddCircle(x, y, s)
                gc.DrawPath(path)
            dc.SetBrush(wx.Brush(name if b else self.foregroundColour))
            dc.DrawCircle(x, y, r)
    
    def blink(self, msec, mask=0):
        """Blinks once for given milliseconds.
        
        >>> self.timer = wx.Timer(self)
        >>> self.timer.Start(1000)
        >>> self.Bind(wx.EVT_TIMER,
                      lambda v: self.indicator.blink(500))
        """
        def _blink():
            if self and self.Value == v & mask:
                self.Value = v
        v = self.Value
        if v and msec:
            self.Value = v & mask
            wx.CallAfter(wx.CallLater, msec, _blink)


class Gauge(wx.Control):
    """Rainbow gauge
    
    Args:
        range   : maximum value
        value   : initial value
        **kwargs: keywords for wx.Control
    """
    @property
    def Value(self):
        return self.__value
    
    @Value.setter
    def Value(self, v):
        self.__value = int(v)
        self.Refresh()
    
    @property
    def Range(self):
        return self.__range
    
    @Range.setter
    def Range(self, v):
        self.__range = int(v)
        self.Refresh()
    
    def __init__(self, parent, range=24, value=0,
                 style=wx.BORDER_NONE, **kwargs):
        wx.Control.__init__(self, parent, style=style, **kwargs)
        
        self.__range = range
        self.__value = value
        
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT) # to avoid flickering
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
    
    def OnSize(self, evt):
        self.Refresh()
    
    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.Clear()
        dc.SetPen(wx.TRANSPARENT_PEN)
        
        def gradients(x):
            y = 4 * x
            if   y < 1: rgb = (0, y, 1)
            elif y < 2: rgb = (0, 1, 2-y)
            elif y < 3: rgb = (y-2, 1, 0)
            else:       rgb = (1, 4-y, 0)
            return [int(255 * x) for x in rgb]
        
        w, h = self.ClientSize
        N = self.__range
        d = max(w//N - 1, 1)
        for i in range(N):
            x = int(i * w / N)
            if i < self.__value:
                dc.SetBrush(wx.Brush(gradients(i/N)))
            else:
                dc.SetBrush(wx.Brush('white'))
            dc.DrawRectangle(x, 0, d, h)
