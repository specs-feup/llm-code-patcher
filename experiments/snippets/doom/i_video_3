void I_StartTic(void) {

    if (!X_display) return;

    while (XPending(X_display))
	    I_GetEvent();

    // Warp the pointer back to the middle of the window
    //  or it will wander off - that is, the game will
    //  loose input focus within X11.
    if (grabMouse)
    {
        if (!--doPointerWarp)
        {
            XWarpPointer(X_display,
                None,
                X_mainWindow,
                0, 0,
                0, 0,
                X_width/2, X_height/2);

            doPointerWarp = POINTER_WARP_COUNTDOWN;
        }
    }

    mousemoved = false;
}