local logger = hs.logger.new("windows", "debug")

--[[
    resizeWindow
]]
function resizeWindow(how)
    logger.df("resizeWindow -- begin")
    logger.df("resizeWindow -- how: %s", how)

    local win = hs.window.focusedWindow()
    local app = win:application():name()

    local frame = screenFrameWithSwitchGlass()
    local newrect

    if how == "left" then
        frame.w = frame.w / 2
        newrect = frame
    elseif how == "right" then
        frame.x = frame.w / 2 + frame.x
        frame.w = frame.w / 2
        newrect = frame
    elseif how == "up" then
        frame.h = frame.h / 2
        logger.df("frame: %s", frame)
        newrect = frame
    elseif how == "down" then
        frame.y = frame.h / 2 + frame.y
        frame.h = frame.h / 2
        logger.df("frame: %s", frame)
        newrect = frame
    -- elseif how == "max" then
    --     -- I don't like this but it actually makes the window in a full-screen mode
    --     newrect = hs.layout.maximized
    elseif how == "left_third" or how == "hthird-0" then
        frame.w = frame.w / 3
        newrect = frame
        logger.df("resizeWindow -- newrect: %.1f, %.1f, %.1f, %.1f", newrect.x, newrect.y, newrect.w, newrect.h)
    elseif how == "middle_third_h" or how == "hthird-1" then
        frame.w = frame.w / 3
        frame.x = frame.w + frame.x
        newrect = frame
        logger.df("resizeWindow -- newrect: %.1f, %.1f, %.1f, %.1f", newrect.x, newrect.y, newrect.w, newrect.h)
    elseif how == "right_third" or how == "hthird-2" then
        frame.w = frame.w / 3
        frame.x = 2 * frame.w + frame.x
        newrect = frame
        logger.df("resizeWindow -- newrect: %.1f, %.1f, %.1f, %.1f", newrect.x, newrect.y, newrect.w, newrect.h)
    elseif how == "top_third" or how == "vthird-0" then
        frame.h = frame.h / 3
        newrect = frame
        logger.df("resizeWindow -- newrect: %.1f, %.1f, %.1f, %.1f", newrect.x, newrect.y, newrect.w, newrect.h)
    elseif how == "middle_third_v" or how == "vthird-1" then
        frame.h = frame.h / 3
        frame.y = frame.h + frame.y
        newrect = frame
        logger.df("resizeWindow -- newrect: %.1f, %.1f, %.1f, %.1f", newrect.x, newrect.y, newrect.w, newrect.h)
    elseif how == "bottom_third" or how == "vthird-2" then
        frame.h = frame.h / 3
        frame.y = 2 * frame.h + frame.y
        newrect = frame
        logger.df("resizeWindow -- newrect: %.1f, %.1f, %.1f, %.1f", newrect.x, newrect.y, newrect.w, newrect.h)
    else
        logger.df("resizeWindow -- how: %s is not a valid option", how)
        return
    end

    win:move(newrect)

    logger.df("resizeWindow -- end")
end

--[[
    get_horizontal_third
]]
function get_horizontal_third(win)
    logger.df("get_horizontal_third -- begin")

    local frame = win:frame()
    local screenFrame = win:screen():frame()

    logger.df("frame.x (%.1f) - screenFrame.x (%.1f) = %.1f", frame.x, screenFrame.x, frame.x - screenFrame.x)
    logger.df("frame.y (%.1f) - screenFrame.y (%.1f) = %.1f", frame.y, screenFrame.y, frame.y - screenFrame.y)

    local relFrame = hs.geometry(frame.x - screenFrame.x, frame.y - screenFrame.y, frame.w, frame.h)

    logger.df("refFrame.x: %.1f", relFrame.x)
    logger.df("screenFrame.w: %.1f", screenFrame.w)

    logger.df("3.01 * relFrame.x (%.1f) / screenFrame.w (%.1f) = %.1f", relFrame.x, screenFrame.w, 3.01 * relFrame.x / screenFrame.w)

    local third = math.ceil(3.01 * relFrame.x / screenFrame.w)
    logger.df("get_horizontal_third -- third: %d", third)

    logger.df("get_horizontal_third -- end")

    return third
end

--[[
    get_vertical_third
]]
function get_vertical_third(win)
    logger.df("get_vertical_third -- begin")

    local frame = win:frame()
    local screenFrame = win:screen():frame()

    logger.df("frame.x (%.1f) - screenFrame.x (%.1f) = %.1f", frame.x, screenFrame.x, frame.x - screenFrame.x)
    logger.df("frame.y (%.1f) - screenFrame.y (%.1f) = %.1f", frame.y, screenFrame.y, frame.y - screenFrame.y)

    local relFrame = hs.geometry(frame.x - screenFrame.x, frame.y - screenFrame.y, frame.w, frame.h)

    logger.df("relFrame.x: %.1f", relFrame.x)
    logger.df("screenFrame.w: %.1f", screenFrame.w)

    logger.df("3.01 * relFrame.y (%.1f) / screenFrame.h (%.1f) = %.1f", relFrame.x, screenFrame.w, 3.01 * relFrame.y / screenFrame.h)

    local third = math.floor(3.01 * relFrame.y / screenFrame.h)
    logger.df("get_vertical_third -- third: %d", third)

    logger.df("get_vertical_third -- end")

    return third
end

--[[
    left_third
]]
function left_third()
    logger.df("left_third -- begin")

    local win = hs.window.focusedWindow()
    local third = get_horizontal_third(win)

    logger.df("left_third -- third: %d", third)
    if third == 0 then
        resizeWindow("hthird-0")
    else
        resizeWindow("hthird-" .. (third - 1))
    end

    logger.df("left_third -- end")
end

--[[
    right_third
]]
function right_third()
    logger.df("right_third -- begin")

    local win = hs.window.focusedWindow()
    local third = get_horizontal_third(win)

    logger.df("right_third -- third: %d", third)
    if third == 2 then
        resizeWindow("hthird-2")
    else
        resizeWindow("hthird-" .. (third + 1))
    end

    logger.df("right_third -- end")
end

--[[
    up_third
]]
function up_third()
    logger.df("up_third -- begin")

    local win = hs.window.focusedWindow()
    local third = get_vertical_third(win)

    logger.df("up_third -- third: %d", third)
    if third == 0 then
        resizeWindow("vthird-0")
    else
        resizeWindow("vthird-" .. (third - 1))
    end
    logger.df("up_third -- end")
end

--[[
    down_third
]]
function down_third()
    logger.df("down_third -- begin")

    local win = hs.window.focusedWindow()
    local third = get_vertical_third(win)

    logger.df("down_third -- third: %d", third)
    if third == 2 then
        resizeWindow("vthird-2")
    else
        resizeWindow("vthird-" .. (third + 1))
    end
    logger.df("down_third -- end")
end

--[[
    screenFrameWithSwitchGlass
    Returns a screen frame without SWITCHGLASS dock
]]
function screenFrameWithSwitchGlass()
    logger.df("screenFrameWithSwitchGlass -- begin")
    local fullFrame = hs.window.focusedWindow():screen():fullFrame()
    logger.df("screenFrameWithSwitchGlass -- fullFrame: %.1f, %.1f, %.1f, %.1f", fullFrame.x, fullFrame.y, fullFrame.w, fullFrame.h)

    local frame = hs.window.focusedWindow():screen():frame()
    frame.w = frame.w - SWITCHGLASS_OFFSET_X
    logger.df("screenFrameWithSwitchGlass -- frame: %.1f, %.1f, %.1f, %.1f", frame.x, frame.y, frame.w, frame.h)

    logger.df("screenFrameWithSwitchGlass -- end")
    return frame
end

--[[
    moveWindowToTopLeft
]]
function moveWindowToTopLeft()
    logger.df("Moving the current window to the top left corner of the current screen")

    local screenFrame = screenFrameWithSwitchGlass()
    local windowFrame = hs.window.focusedWindow():frame()

    windowFrame.x = screenFrame.x
    windowFrame.y = screenFrame.y

    logger.df("windowFrame: %.1f, %.1f, %.1f, %.1f", windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)
    hs.window.focusedWindow():move(windowFrame)
end

--[[
    moveWindowToTopCenter
]]
function moveWindowToTopCenter()
    logger.df("Moving the current window to the top center of the current screen")

    local screenFrame = screenFrameWithSwitchGlass()
    local windowFrame = hs.window.focusedWindow():frame()

    logger.df("screenFrame: %.1f, %.1f, %.1f, %.1f", screenFrame.x, screenFrame.y, screenFrame.w, screenFrame.h)

    windowFrame.x = (screenFrame.w / 2) - (windowFrame.w / 2) + screenFrame.x
    windowFrame.y = screenFrame.y

    logger.df("windowFrame: %.1f, %.1f, %.1f, %.1f", windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)
    hs.window.focusedWindow():move(windowFrame)
end

--[[
    moveWindowToTopRight
]]
function moveWindowToTopRight()
    logger.df("Moving the current window to the top right corner of the current screen")

    local screenFrame = screenFrameWithSwitchGlass()
    local windowFrame = hs.window.focusedWindow():frame()

    windowFrame.x = screenFrame.x + (screenFrame.w - windowFrame.w)
    windowFrame.y = screenFrame.y

    logger.df("windowFrame: %.1f, %.1f, %.1f, %.1f", windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)
    hs.window.focusedWindow():move(windowFrame)
end

--[[
    moveWindowToMiddleLeft
]]
function moveWindowToMiddleLeft()
    logger.df("Moving the current window to the middle left of the current screen")

    local screenFrame = screenFrameWithSwitchGlass()
    local windowFrame = hs.window.focusedWindow():frame()

    windowFrame.x = screenFrame.x
    windowFrame.y = screenFrame.y + (screenFrame.h - windowFrame.h) / 2

    logger.df("windowFrame: %.1f, %.1f, %.1f, %.1f", windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)
    hs.window.focusedWindow():move(windowFrame)
end

--[[
    moveWindowToMiddleCenter
]]
function moveWindowToMiddleCenter()
    logger.df("Moving the current window to the middle center of the main screen ...")

    local screenFrame = screenFrameWithSwitchGlass()
    local windowFrame = hs.window.focusedWindow():frame()

    logger.df("screenFrame: %.1f, %.1f, %.1f, %.1f", screenFrame.x, screenFrame.y, screenFrame.w, screenFrame.h)

    windowFrame.x = (screenFrame.w / 2) - (windowFrame.w / 2) + (screenFrame.x)
    windowFrame.y = screenFrame.y + (screenFrame.h - windowFrame.h) / 2

    logger.df("windowFrame: %.1f, %.1f, %.1f, %.1f", windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)
    hs.window.focusedWindow():move(windowFrame)
end

--[[
    moveWindowToMiddleRight
]]
function moveWindowToMiddleRight()
    logger.df("Moving the current window to the middle right of the current screen")

    local screenFrame = screenFrameWithSwitchGlass()
    local windowFrame = hs.window.focusedWindow():frame()

    windowFrame.x = screenFrame.x + (screenFrame.w - windowFrame.w)
    windowFrame.y = screenFrame.y + (screenFrame.h - windowFrame.h) / 2

    logger.df("windowFrame: %.1f, %.1f, %.1f, %.1f", windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)
    hs.window.focusedWindow():move(windowFrame)
end

--[[
    moveWindowToBottomLeft
]]
function moveWindowToBottomLeft()
    logger.df("Moving the current window to the bottom left corner of the current screen")

    local screenFullFrame = hs.window.focusedWindow():screen():fullFrame()
    local screenFrame = screenFrameWithSwitchGlass()
    local windowFrame = hs.window.focusedWindow():frame()

    windowFrame.x = screenFrame.x
    windowFrame.y = screenFullFrame.h - windowFrame.h

    logger.df("windowFrame: %.1f, %.1f, %.1f, %.1f", windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)
    hs.window.focusedWindow():move(windowFrame)
end

--[[
    moveWindowToBottomCenter
]]
function moveWindowToBottomCenter()
    logger.df("Moving the current window to the bottom center of the current screen")

    local screenFullFrame = hs.window.focusedWindow():screen():fullFrame()
    local screenFrame = screenFrameWithSwitchGlass()
    local windowFrame = hs.window.focusedWindow():frame()

    windowFrame.x = (screenFrame.w / 2) - (windowFrame.w / 2) + screenFrame.x
    windowFrame.y = screenFullFrame.h - windowFrame.h

    logger.df("windowFrame: %.1f, %.1f, %.1f, %.1f", windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)
    hs.window.focusedWindow():move(windowFrame)
end

--[[
    moveWindowToBottomRight
]]
function moveWindowToBottomRight()
    logger.df("Moving the current window to the bottom right corner of the current screen")

    local screenFullFrame = hs.window.focusedWindow():screen():fullFrame()
    local windowFrame = hs.window.focusedWindow():frame()

    windowFrame.x = screenFullFrame.x + (screenFullFrame.w - SWITCHGLASS_OFFSET_X) - windowFrame.w
    windowFrame.y = screenFullFrame.h - windowFrame.h

    logger.df("windowFrame: %.1f, %.1f, %.1f, %.1f", windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)
    hs.window.focusedWindow():move(windowFrame)
end

--[[
    resizeWindowToTopLeftThird
]]
function resizeWindowToTopLeftThird()
    logger.df("resizeWindowToTopLeftThird")

    local screenFrame = hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    logger.df("screenFrame: %.1f, %.1f, %.1f, %.1f", screenFrame.x, screenFrame.y, screenFrame.w, screenFrame.h)
    logger.df("windowFrame: %.1f, %.1f, %.1f, %.1f", windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)

    local width = (screenFrame.w - SWITCHGLASS_OFFSET_X) / 3
    local height = screenFrame.h / 2

    local rect = hs.geometry.rect(screenFrame.x, screenFrame.y, width, height)
    logger.df("rect: %.1f, %.1f, %.1f, %.1f", rect.x, rect.y, rect.w, rect.h)

    hs.window.focusedWindow():move(rect)
end

--[[
    resizeWindowToTopCenterThird
]]
function resizeWindowToTopCenterThird()
    logger.df("resizeWindowToTopCenterThird")

    local screenFrame = hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    logger.df("screenFrame: %.1f, %.1f, %.1f, %.1f", screenFrame.x, screenFrame.y, screenFrame.w, screenFrame.h)
    logger.df("windowFrame: %.1f, %.1f, %.1f, %.1f", windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)

    local width = (screenFrame.w - SWITCHGLASS_OFFSET_X) / 3
    local height = screenFrame.h / 2

    local rect = hs.geometry.rect(screenFrame.x, screenFrame.y, width, height)
    local rect = hs.geometry.rect(width, screenFrame.y, width, height)
    logger.df("rect: %.1f, %.1f, %.1f, %.1f", rect.x, rect.y, rect.w, rect.h)

    hs.window.focusedWindow():move(rect)
end

--[[
    resizeWindowToTopRightThird
]]
function resizeWindowToTopRightThird()
    logger.df("resizeWindowToTopRightThird")

    local screenFrame = hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    logger.df("screenFrame: %.1f, %.1f, %.1f, %.1f", screenFrame.x, screenFrame.y, screenFrame.w, screenFrame.h)
    logger.df("windowFrame: %.1f, %.1f, %.1f, %.1f", windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)

    local width = (screenFrame.w - SWITCHGLASS_OFFSET_X) / 3
    local height = screenFrame.h / 2

    local rect = hs.geometry.rect(screenFrame.x, screenFrame.y, width, height)
    local rect = hs.geometry.rect(width * 2, screenFrame.y, width, height)
    logger.df("rect: %.1f, %.1f, %.1f, %.1f", rect.x, rect.y, rect.w, rect.h)

    hs.window.focusedWindow():move(rect)
end

--[[
    resizeWindowToBottomLeftThird
]]
function resizeWindowToBottomLeftThird()
    logger.df("resizeWindowToBottomLeftThird")

    local screenFrame = hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    logger.df("screenFrame: %.1f, %.1f, %.1f, %.1f", screenFrame.x, screenFrame.y, screenFrame.w, screenFrame.h)
    logger.df("windowFrame: %.1f, %.1f, %.1f, %.1f", windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)

    local width = (screenFrame.w - SWITCHGLASS_OFFSET_X) / 3
    local height = screenFrame.h / 2

    local rect = hs.geometry.rect(screenFrame.x, screenFrame.y + height, width, height)
    logger.df("rect: %.1f, %.1f, %.1f, %.1f", rect.x, rect.y, rect.w, rect.h)

    hs.window.focusedWindow():move(rect)
end

--[[
    resizeWindowToBottomCenterThird
]]
function resizeWindowToBottomCenterThird()
    logger.df("moveWindowBottomCenterThird")

    local screenFrame = hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    logger.df("screenFrame: %.1f, %.1f, %.1f, %.1f", screenFrame.x, screenFrame.y, screenFrame.w, screenFrame.h)
    logger.df("windowFrame: %.1f, %.1f, %.1f, %.1f", windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)

    local width = (screenFrame.w - SWITCHGLASS_OFFSET_X) / 3
    local height = screenFrame.h / 2

    local rect = hs.geometry.rect(width, screenFrame.y + height, width, height)
    logger.df("rect: %.1f, %.1f, %.1f, %.1f", rect.x, rect.y, rect.w, rect.h)

    hs.window.focusedWindow():move(rect)
end

--[[
    resizeWindowToBottomRightThird
]]
function resizeWindowToBottomRightThird()
    logger.df("resizeWindowToBottomRightThird")

    local screenFrame = hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    logger.df("screenFrame: %.1f, %.1f, %.1f, %.1f", screenFrame.x, screenFrame.y, screenFrame.w, screenFrame.h)
    logger.df("windowFrame: %.1f, %.1f, %.1f, %.1f", windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)

    local width = (screenFrame.w - SWITCHGLASS_OFFSET_X) / 3
    local height = screenFrame.h / 2

    local rect = hs.geometry.rect(width * 2, screenFrame.y + height, width, height)
    logger.df("rect: %.1f, %.1f, %.1f, %.1f", rect.x, rect.y, rect.w, rect.h)

    hs.window.focusedWindow():move(rect)
end

--[[
    moveWindowToOneScreenEast
]]
function moveWindowToOneScreenEast()
    logger.df("moveWindowToOneScreenEast")

    if hs.screen.mainScreen():toEast() == nil then
        logger.df("There are no screens on the right")
        return
    end

    local destScreenFrame = hs.screen.mainScreen():toEast():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    logger.df("destScreenFrame: %.1f, %.1f, %.1f, %.1f", destScreenFrame.x, destScreenFrame.y, destScreenFrame.w, destScreenFrame.h)
    logger.df("windowFrame: %.1f, %.1f, %.1f, %.1f", windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)

    local size = windowFrame.size
    if windowFrame.w > destScreenFrame.w then
        size.w = destScreenFrame.w - SWITCHGLASS_OFFSET_X
    end

    if windowFrame.h > destScreenFrame.h then
        size.h = destScreenFrame.h
    end

    hs.window.focusedWindow():setSize(size)
    hs.window.focusedWindow():moveOneScreenEast(true, true)

    local appName = hs.application.frontmostApplication():name()
    logger.df("appName: " .. appName)

    if appName == "iTerm2" then
        local windowFrame = hs.window.focusedWindow():frame()
        logger.df("windowFrame: " .. windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)

        if windowFrame.w < ITERM2_WINDOW_WIDTH then
            windowFrame.x = windowFrame.x - (ITERM2_WINDOW_WIDTH - windowFrame.w)
            windowFrame.w = ITERM2_WINDOW_WIDTH
            hs.window.focusedWindow():move(windowFrame)
        end
    end
end

--[[
    moveWindowToOneScreenWest
]]
function moveWindowToOneScreenWest()
    logger.df("moveWindowToOneScreenWest")

    if hs.screen.mainScreen():toWest() == nil then
        logger.df("There are no screens on the left")
        return
    end

    local destScreenFrame = hs.screen.mainScreen():toWest():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    logger.df("destScreenFrame: " .. destScreenFrame.x, destScreenFrame.y, destScreenFrame.w, destScreenFrame.h)
    logger.df("windowFrame: " .. windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)

    local size = windowFrame.size
    if windowFrame.w > destScreenFrame.w then
        size.w = destScreenFrame.w - SWITCHGLASS_OFFSET_X
    end

    if windowFrame.h > destScreenFrame.h then
        size.h = destScreenFrame.h
    end
    hs.window.focusedWindow():setSize(size)
    hs.window.focusedWindow():moveOneScreenWest(true, true)

    local appName = hs.application.frontmostApplication():name()
    logger.df("appName: " .. appName)

    if appName == "iTerm2" then
        local windowFrame = hs.window.focusedWindow():frame()
        logger.df("windowFrame: %.1f, %.1f, %.1f, %.1f" .. windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)

        if windowFrame.w < ITERM2_WINDOW_WIDTH then
            windowFrame.x = windowFrame.x - (ITERM2_WINDOW_WIDTH - windowFrame.w)
            windowFrame.w = ITERM2_WINDOW_WIDTH
            hs.window.focusedWindow():move(windowFrame)
        end
    end
end

--[[
    maximizeWindow
]]
function maximizeWindow()
    local frame = hs.screen.mainScreen():frame()
    local fullFrame = hs.screen.mainScreen():fullFrame()

    logger.df("Maximizing the current window ...")
    logger.df("frame: %s", frame)
    logger.df("fullFrame: %s", fullFrame)

    -- Ensure that the maximized window is not covered by the SwitchGlass application switcher
    local rect = hs.geometry.rect(frame.x, frame.y, frame.w - SWITCHGLASS_OFFSET_X, frame.h)
    hs.window.focusedWindow():move(rect)
end

-- Bind the window movement functions to keyboard shortcuts

-- These are from https://github.com/wangshub/hammerspoon-config/blob/master/window/window.lua

--[[
The following four functions resize the front window to top-half, bottom-half, left-half or
right-half, depending on the user input.
]]
hs.hotkey.bind({"cmd", "ctrl"}, "Left", hs.fnutils.partial(resizeWindow, "left"))
hs.hotkey.bind({"cmd", "ctrl"}, "Right", hs.fnutils.partial(resizeWindow, "right"))
hs.hotkey.bind({"cmd", "ctrl"}, "Up", hs.fnutils.partial(resizeWindow, "up"))
hs.hotkey.bind({"cmd", "ctrl"}, "Down", hs.fnutils.partial(resizeWindow, "down"))

--[[
The following four functions resize the front window to top-third, middle-third (vertical),
bottom-third, left-third, middle-third (horizontal) or right-third, depending on user input.

The front window resizes its length (or height) to its maximum.
]]
hs.hotkey.bind({"ctrl", "alt"}, "Left", left_third)
hs.hotkey.bind({"ctrl", "alt"}, "Right", right_third)
hs.hotkey.bind({"ctrl", "alt"}, "Up", up_third)
hs.hotkey.bind({"ctrl", "alt"}, "Down", down_third)

hs.hotkey.bind({"cmd", "ctrl", "alt"}, "F", hs.fnutils.partial(resizeWindow, "max"))

-- The rest are mine

--[[
The following nine functions only move the front window to a new position.
The function does not resize the window in any way at all.
]]
hs.hotkey.bind({"cmd", "ctrl"}, "U", moveWindowToTopLeft)
hs.hotkey.bind({"cmd", "ctrl"}, "I", moveWindowToTopCenter)
hs.hotkey.bind({"cmd", "ctrl"}, "O", moveWindowToTopRight)

hs.hotkey.bind({"cmd", "ctrl"}, "J", moveWindowToMiddleLeft)
hs.hotkey.bind({"cmd", "ctrl"}, "K", moveWindowToMiddleCenter)
hs.hotkey.bind({"cmd", "ctrl"}, "L", moveWindowToMiddleRight)

hs.hotkey.bind({"cmd", "ctrl"}, "M", moveWindowToBottomLeft)
hs.hotkey.bind({"cmd", "ctrl"}, ".", moveWindowToBottomRight)
hs.hotkey.bind({"cmd", "ctrl"}, ",", moveWindowToBottomCenter)

--[[
The following six functions move the front window to a new position;
- top-left, top-center, top-right, bottom-left, bottom-center and bottom-right

Also, the height of the window is changed to 50% of the screen height.
]]
hs.hotkey.bind({"ctrl", "alt"}, "U", resizeWindowToTopLeftThird)
hs.hotkey.bind({"ctrl", "alt"}, "I", resizeWindowToTopCenterThird)
hs.hotkey.bind({"ctrl", "alt"}, "O", resizeWindowToTopRightThird)
hs.hotkey.bind({"ctrl", "alt"}, "M", resizeWindowToBottomLeftThird)
hs.hotkey.bind({"ctrl", "alt"}, ",", resizeWindowToBottomCenterThird)
hs.hotkey.bind({"ctrl", "alt"}, ".", resizeWindowToBottomRightThird)

--[[
The following two functions move the front window to adjacent screen, if available.
Nothing happens otherwise.
]]
hs.hotkey.bind({"cmd", "ctrl", "shift"}, "L", moveWindowToOneScreenEast)
hs.hotkey.bind({"cmd", "ctrl", "shift"}, "J", moveWindowToOneScreenWest)
hs.hotkey.bind({"cmd", "ctrl"}, "Z", maximizeWindow)
