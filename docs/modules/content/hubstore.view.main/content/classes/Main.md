Back to [All Modules](https://github.com/pyrustic/hubstore/blob/master/docs/modules/README.md#readme)

# Module Overview

**hubstore.view.main**
 
No description

> **Classes:** &nbsp; [Main](https://github.com/pyrustic/hubstore/blob/master/docs/modules/content/hubstore.view.main/content/classes/Main.md#class-main)
>
> **Functions:** &nbsp; None
>
> **Constants:** &nbsp; None

# Class Main
Subclass this if you are going to create a view.

Lifecycle of a view:
    1- you instantiate the view
    2- '__init__()' is implicitly called
    3- you call the method '.build()'
    4- '_build()' is implicitly called
    5- '_on_map()' is implicitly called once the widget is mapped
    6- '_on_destroy()' is implicitly called when the widget is destroyed/closed

The rules to create your view is simple:
- You need to subclass Viewable.
- You need to implement the methods '_build()', and optionally
    implement '_on_map()' and '_on_destroy()'.
- You need to set an instance variable '_body' with either a tk.Frame or tk.Toplevel
    in the method '_on_build()'
That's all ! Of course, when you are ready to use the view, just call the 'build()' method.
Calling the 'build()' method will return the body of the view. The one that you assigned
to the instance variable '_body'. The same body can be retrieved with the property 'body'.
The 'build()' method should be called once. Calling it more than once will still return
the body object, but the view won't be built again.
You can't re-build your same view instance after destroying its body.
You can destroy the body directly, by calling the conventional tkinter destruction method
 on the view's body. But it's recommended to destroy the view by calling the view's method
 'destroy()' inherited from the class Viewable.
The difference between these two ways of destruction is that when u call the Viewable's
 'destroy()' method, the method '_on_destroy()' will be called BEFORE the effective
 destruction of the body. If u call directly 'destroy' conventionally on the tkinter
 object (the body), the method '_on_destroy()' will be called AFTER the beginning
  of destruction of the body.

  By the way, you can use convenience methods "build_pack", "build_grid", "build_place"
  to build and pack/grid/place your widget in the master !!
  Use "build_wait" for toplevels if you want the app to wait till the window closes

## Base Classes
viewable.Viewable

## Class Attributes


## Class Properties
|Property|Type|Description|Inherited from|
|---|---|---|---|
|app|getter|None||
|body|getter|Get the body of this view.|viewable.Viewable|
|host|getter|None||
|views|getter|None||



# All Methods
[\_\_init\_\_](#__init__) &nbsp;&nbsp; [\_binding](#_binding) &nbsp;&nbsp; [\_build](#_build) &nbsp;&nbsp; [\_install\_pane](#_install_pane) &nbsp;&nbsp; [\_install\_toolbar](#_install_toolbar) &nbsp;&nbsp; [\_on\_destroy](#_on_destroy) &nbsp;&nbsp; [\_on\_map](#_on_map) &nbsp;&nbsp; [build](#build) &nbsp;&nbsp; [build\_grid](#build_grid) &nbsp;&nbsp; [build\_pack](#build_pack) &nbsp;&nbsp; [build\_place](#build_place) &nbsp;&nbsp; [build\_wait](#build_wait) &nbsp;&nbsp; [clear\_notification](#clear_notification) &nbsp;&nbsp; [close\_toast](#close_toast) &nbsp;&nbsp; [open\_toplevel\_about](#open_toplevel_about) &nbsp;&nbsp; [open\_toplevel\_info](#open_toplevel_info) &nbsp;&nbsp; [open\_toplevel\_installer](#open_toplevel_installer) &nbsp;&nbsp; [open\_toplevel\_openlist](#open_toplevel_openlist) &nbsp;&nbsp; [open\_toplevel\_promoted](#open_toplevel_promoted) &nbsp;&nbsp; [open\_toplevel\_report](#open_toplevel_report) &nbsp;&nbsp; [show\_notification](#show_notification) &nbsp;&nbsp; [show\_toast](#show_toast)

## \_\_init\_\_
Initialize self.  See help(type(self)) for accurate signature.



**Signature:** (self, app)





**Return Value:** None.

[Back to Top](#module-overview)


## \_binding
None



**Signature:** (self)





**Return Value:** None.

[Back to Top](#module-overview)


## \_build
Build the view layout here



**Signature:** (self)





**Return Value:** None.

[Back to Top](#module-overview)


## \_install\_pane
None



**Signature:** (self)





**Return Value:** None.

[Back to Top](#module-overview)


## \_install\_toolbar
None



**Signature:** (self)





**Return Value:** None.

[Back to Top](#module-overview)


## \_on\_destroy
Put here the code that will be executed at destroy event

**Inherited from:** viewable.Viewable

**Signature:** (self)





**Return Value:** None.

[Back to Top](#module-overview)


## \_on\_map
Put here the code that will be executed once
the body is mapped.



**Signature:** (self)





**Return Value:** None.

[Back to Top](#module-overview)


## build
Build this view 

**Inherited from:** viewable.Viewable

**Signature:** (self)





**Return Value:** None.

[Back to Top](#module-overview)


## build\_grid
Build this view then grid it 

**Inherited from:** viewable.Viewable

**Signature:** (self, cnf=None, \*\*kwargs)





**Return Value:** None.

[Back to Top](#module-overview)


## build\_pack
Build this view then pack it 

**Inherited from:** viewable.Viewable

**Signature:** (self, cnf=None, \*\*kwargs)





**Return Value:** None.

[Back to Top](#module-overview)


## build\_place
Build this view then place it 

**Inherited from:** viewable.Viewable

**Signature:** (self, cnf=None, \*\*kwargs)





**Return Value:** None.

[Back to Top](#module-overview)


## build\_wait
Build this view then wait till it closes.
The view should have a tk.Toplevel as body 

**Inherited from:** viewable.Viewable

**Signature:** (self)





**Return Value:** None.

[Back to Top](#module-overview)


## clear\_notification
None



**Signature:** (self)





**Return Value:** None.

[Back to Top](#module-overview)


## close\_toast
None



**Signature:** (self)





**Return Value:** None.

[Back to Top](#module-overview)


## open\_toplevel\_about
None



**Signature:** (self)





**Return Value:** None.

[Back to Top](#module-overview)


## open\_toplevel\_info
None



**Signature:** (self, data)





**Return Value:** None.

[Back to Top](#module-overview)


## open\_toplevel\_installer
None



**Signature:** (self, data)





**Return Value:** None.

[Back to Top](#module-overview)


## open\_toplevel\_openlist
None



**Signature:** (self, data)





**Return Value:** None.

[Back to Top](#module-overview)


## open\_toplevel\_promoted
None



**Signature:** (self, data)





**Return Value:** None.

[Back to Top](#module-overview)


## open\_toplevel\_report
None



**Signature:** (self, data)





**Return Value:** None.

[Back to Top](#module-overview)


## show\_notification
None



**Signature:** (self, message)





**Return Value:** None.

[Back to Top](#module-overview)


## show\_toast
None



**Signature:** (self, message, duration=1234)





**Return Value:** None.

[Back to Top](#module-overview)



