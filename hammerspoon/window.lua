local logger = hs.logger.new("windows", "debug")

function winresize(how)
    local win = hs.window.focusedWindow()
    local app = win:application():name()
    local windowLayout
    local newrect

    logger.df("how: %s", how)

    if how == "left" then
        newrect = hs.layout.left50
    elseif how == "right" then
        newrect = hs.layout.right50
    elseif how == "up" then
        newrect = {0, 0, 1, 0.5}
    elseif how == "down" then
        newrect = {0, 0.5, 1, 0.5}
    elseif how == "max" then
        -- I don't like this but it actually makes the window in a full-screen mode
        newrect = hs.layout.maximized
    elseif how == "left_third" or how == "hthird-0" then
        newrect = {0, 0, 1/3, 1}
    elseif how == "middle_third_h" or how == "hthird-1" then
        newrect = {1/3, 0, 1/3, 1}
    elseif how == "right_third" or how == "hthird-2" then
        newrect = {2/3, 0, 1/3, 1}
    elseif how == "top_third" or how == "vthird-0" then
        newrect = {0, 0, 1, 1/3}
    elseif how == "middle_third_v" or how == "vthird-1" then
        newrect = {0, 1/3, 1, 1/3}
    elseif how == "bottom_third" or how == "vthird-2" then
        newrect = {0, 2/3, 1, 1/3}
    end

    win:move(newrect)
end

function get_horizontal_third(win)
    local frame = win:frame()
    local screenFrame = win:screen():frame()
    local relFrame = hs.geometry(frame.x - screenFrame.x, frame.y - screenFrame.y, frame.w, frame.h)
    local third = math.floor(3.01 * relFrame.x / screenFrame.w)

    logger.df("Screen frame: %s", screenFrame)
    logger.df("Window frame: %s, relFrame %s is in horizontal third %d", frame, relFrame, third)
    return third
end

function get_vertical_third(win)
    local frame = win:frame()
    local screenFrame = win:screen():frame()
    local relFrame = hs.geometry(frame.x - screenFrame.x, frame.y - screenFrame.y, frame.w, frame.h)
    local third = math.floor(3.01 * relFrame.y / screenFrame.h)

    logger.df("Screen frame: %s", screenFrame)
    logger.df("Window frame: %s, relFrame %s is in vertical third %d", frame, relFrame, third)
    return third
end

function left_third()
    local win = hs.window.focusedWindow()
    local third = get_horizontal_third(win)
    if third == 0 then
        winresize("hthird-0")
    else
        winresize("hthird-" .. (third - 1))
    end
end

function right_third()
    local win = hs.window.focusedWindow()
    local third = get_horizontal_third(win)
    if third == 2 then
        winresize("hthird-2")
    else
        winresize("hthird-" .. (third + 1))
    end
end

function up_third()
    local win = hs.window.focusedWindow()
    local third = get_vertical_third(win)
    if third == 0 then
        winresize("vthird-0")
    else
        winresize("vthird-" .. (third - 1))
    end
end

function down_third()
    local win = hs.window.focusedWindow()
    local third = get_vertical_third(win)
    if third == 2 then
        winresize("vthird-2")
    else
        winresize("vthird-" .. (third + 1))
    end
end

function screenFrameWithSwitchGlass()
    local fullFrame = hs.window.focusedWindow():screen():fullFrame()
    local frame = hs.window.focusedWindow():screen():frame()

    logger.df("fullFrame: %s", fullFrame)
    logger.df("frame: %s", frame)

    frame.w = frame.w - SWITCHGLASS_OFFSET_X
    logger.df("frame: %s", frame)

    return frame
end

--[[
moveWindowToTopLeft
]]
function moveWindowToTopLeft()
    logger.df("Moving the current window to the top left corner of the current screen")

    -- Take note of the menu bar and also the dock
    local screenFrame = screenFrameWithSwitchGlass() -- hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    windowFrame.x = screenFrame.x
    windowFrame.y = screenFrame.y

    logger.df("windowFrame: %s", windowFrame)
    hs.window.focusedWindow():move(windowFrame)
end

--[[
moveWindowToTopCenter
]]
function moveWindowToTopCenter()
    logger.df("Moving the current window to the top center of the current screen")

    local screenFrame = screenFrameWithSwitchGlass() -- hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    logger.df("screenFrame: %s", screenFrame)
    logger.df("windowFrame: %s", windowFrame)

    windowFrame.x = (screenFrame.w / 2) - (windowFrame.w / 2) + screenFrame.x
    windowFrame.y = screenFrame.y

    logger.df("windowFrame: %s", windowFrame)
    hs.window.focusedWindow():move(windowFrame)
end

--[[
moveWindowToTopRight
]]
function moveWindowToTopRight()
    logger.df("Moving the current window to the top right corner of the current screen")

    local screenFrame = screenFrameWithSwitchGlass() -- hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    windowFrame.x = screenFrame.x + (screenFrame.w - windowFrame.w)
    windowFrame.y = screenFrame.y

    logger.df("windowFrame: %s", windowFrame)
    hs.window.focusedWindow():move(windowFrame)
end

--[[
moveWindowToLeftCenter
]]
function moveWindowToLeftCenter()
    print("Moving the current window to the left center of the current screen")

    local screenFrame = screenFrameWithSwitchGlass() -- hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    windowFrame.x = screenFrame.x
    windowFrame.y = screenFrame.y + (screenFrame.h - windowFrame.h) / 2

    print("windowFrame: " .. windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)
    hs.window.focusedWindow():move(windowFrame)
end

--[[
moveWindowToCenter
]]
function moveWindowToCenter()
    logger.df("Moving the current window to the center of the main screen ...")

    local screenFrame = screenFrameWithSwitchGlass() -- hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    logger.df("screenFrame: %s", screenFrame)
    logger.df("windowFrame: %s", windowFrame)

    windowFrame.x = (screenFrame.w / 2) - (windowFrame.w / 2) + (screenFrame.x)
    windowFrame.y = screenFrame.y + (screenFrame.h - windowFrame.h) / 2

    logger.df("windowFrame: %s", windowFrame)
    hs.window.focusedWindow():move(windowFrame)
end

--[[
moveWindowToRightCenter
]]
function moveWindowToRightCenter()
    logger.df("Moving the current window to the right center of the current screen")

    local screenFrame = screenFrameWithSwitchGlass() --hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    windowFrame.x = screenFrame.x + (screenFrame.w - windowFrame.w)
    windowFrame.y = screenFrame.y + (screenFrame.h - windowFrame.h) / 2

    logger.df("windowFrame: %s", windowFrame)
    hs.window.focusedWindow():move(windowFrame)
end

--[[
moveWindowToBottomLeft
]]
function moveWindowToBottomLeft()
    logger.df("Moving the current window to the bottom left corner of the current screen")

    local screenFullFrame = hs.window.focusedWindow():screen():fullFrame()
    local screenFrame = screenFrameWithSwitchGlass() --hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    windowFrame.x = screenFrame.x
    windowFrame.y = screenFullFrame.h - windowFrame.h

    logger.df("windowFrame: %s", windowFrame)
    hs.window.focusedWindow():move(windowFrame)
end

--[[
moveWindowToBottomCenter
]]
function moveWindowToBottomCenter()
    print("Moving the current window to the bottom center of the current screen")

    local screenFullFrame = hs.window.focusedWindow():screen():fullFrame()
    local screenFrame = screenFrameWithSwitchGlass() -- hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    windowFrame.x = (screenFrame.w / 2) - (windowFrame.w / 2) + screenFrame.x
    windowFrame.y = screenFullFrame.h - windowFrame.h

    logger.df("windowFrame: %s", windowFrame)
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

    logger.df("windowFrame: %s", windowFrame)
    hs.window.focusedWindow():move(windowFrame)
end

--[[
resizeWindowToTopLeftThird
]]
function resizeWindowToTopLeftThird()
    print("resizeWindowToTopLeftThird")

    local screenFrame = hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    local width = (screenFrame.w - SWITCHGLASS_OFFSET_X) / 3
    local height = screenFrame.h / 2
    local rect = hs.geometry.rect(screenFrame.x, screenFrame.y, width, height)

    hs.window.focusedWindow():move(rect)
end

--[[
resizeWindowToTopCenterThird
]]
function resizeWindowToTopCenterThird()
    print("resizeWindowToTopCenterThird")

    local screenFrame = hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    local width = (screenFrame.w - SWITCHGLASS_OFFSET_X) / 3
    local height = screenFrame.h / 2
    local rect = hs.geometry.rect(screenFrame.x, screenFrame.y, width, height)

    local rect = hs.geometry.rect(width, screenFrame.y, width, height)
    hs.window.focusedWindow():move(rect)
end

--[[
resizeWindowToTopRightThird
]]
function resizeWindowToTopRightThird()
    print("resizeWindowToTopRightThird")

    local screenFrame = hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    local width = (screenFrame.w - SWITCHGLASS_OFFSET_X) / 3
    local height = screenFrame.h / 2
    local rect = hs.geometry.rect(screenFrame.x, screenFrame.y, width, height)

    local rect = hs.geometry.rect(width * 2, screenFrame.y, width, height)
    hs.window.focusedWindow():move(rect)
end

--[[
resizeWindowToBottomLeftThird
]]
function resizeWindowToBottomLeftThird()
    print("resizeWindowToBottomLeftThird")

    local screenFrame = hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    local width = (screenFrame.w - SWITCHGLASS_OFFSET_X) / 3
    local height = screenFrame.h / 2
    local rect = hs.geometry.rect(screenFrame.x, screenFrame.y + height, width, height)

    hs.window.focusedWindow():move(rect)
end

--[[
resizeWindowToBottomCenterThird
]]
function resizeWindowToBottomCenterThird()
    print("moveWindowBottomCenterThird")

    local screenFrame = hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    local width = (screenFrame.w - SWITCHGLASS_OFFSET_X) / 3
    local height = screenFrame.h / 2
    local rect = hs.geometry.rect(width, screenFrame.y + height, width, height)

    hs.window.focusedWindow():move(rect)
end

--[[
resizeWindowToBottomRightThird
]]
function resizeWindowToBottomRightThird()
    print("resizeWindowToBottomRightThird")

    local screenFrame = hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    local width = (screenFrame.w - SWITCHGLASS_OFFSET_X) / 3
    local height = screenFrame.h / 2
    local rect = hs.geometry.rect(width * 2, screenFrame.y + height, width, height)

    hs.window.focusedWindow():move(rect)
end

--[[
moveWindowToOneScreenEast
]]
function moveWindowToOneScreenEast()
    print("moveWindowToOneScreenEast")

    if hs.screen.mainScreen():toEast() == nil then
        print("There are no screens on the right")
        return
    end

    local destScreenFrame = hs.screen.mainScreen():toEast():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    print("destScreenFrame: " .. destScreenFrame.x, destScreenFrame.y, destScreenFrame.w, destScreenFrame.h)
    print("windowFrame: " .. windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)

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
    print("appName: " .. appName)

    if appName == "iTerm2" then
        local windowFrame = hs.window.focusedWindow():frame()
        print("windowFrame: " .. windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)

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
    print("moveWindowToOneScreenWest")

    if hs.screen.mainScreen():toWest() == nil then
        print("There are no screens on the left")
        return
    end

    local destScreenFrame = hs.screen.mainScreen():toWest():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    print("destScreenFrame: " .. destScreenFrame.x, destScreenFrame.y, destScreenFrame.w, destScreenFrame.h)
    print("windowFrame: " .. windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)

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
    print("appName: " .. appName)

    if appName == "iTerm2" then
        local windowFrame = hs.window.focusedWindow():frame()
        print("windowFrame: " .. windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)

        if windowFrame.w < ITERM2_WINDOW_WIDTH then
            windowFrame.x = windowFrame.x - (ITERM2_WINDOW_WIDTH - windowFrame.w)
            windowFrame.w = ITERM2_WINDOW_WIDTH
            hs.window.focusedWindow():move(windowFrame)
        end
    end
end

function maximizeWindow()
    local frame = hs.screen.mainScreen():frame()
    local fullFrame = hs.screen.mainScreen():fullFrame()

    logger.df("Maximizing the current window ...")
    logger.df("frame: %s", frame)
    logger.df("fullFrame: %s", fullFrame)
    -- print("Maximizing the current window ...")
    -- print("frame: " .. frame.x, frame.y, frame.w, frame.h)
    -- print("fullFrame: " .. fullFrame.x, fullFrame.y, fullFrame.w, fullFrame.h)

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
hs.hotkey.bind({"cmd", "ctrl"}, "Left", hs.fnutils.partial(winresize, "left"))
hs.hotkey.bind({"cmd", "ctrl"}, "Right", hs.fnutils.partial(winresize, "right"))
hs.hotkey.bind({"cmd", "ctrl"}, "Up", hs.fnutils.partial(winresize, "up"))
hs.hotkey.bind({"cmd", "ctrl"}, "Down", hs.fnutils.partial(winresize, "down"))

--[[
The following four functions resize the front window to top-third, middle-third (vertical),
bottom-third, left-third, middle-third (horizontal) or right-third, depending on user input.

The front window resizes its length (or height) to its maximum.
]]
hs.hotkey.bind({"ctrl", "alt"}, "Left", left_third)
hs.hotkey.bind({"ctrl", "alt"}, "Right", right_third)
hs.hotkey.bind({"ctrl", "alt"}, "Up", up_third)
hs.hotkey.bind({"ctrl", "alt"}, "Down", down_third)

hs.hotkey.bind({"cmd", "ctrl", "alt"}, "F", hs.fnutils.partial(winresize, "max"))

-- The rest are mine

--[[
The following nine functions only move the front window to a new position.
The function does not resize the window in any way at all.
]]
hs.hotkey.bind({"cmd", "ctrl"}, "U", moveWindowToTopLeft)
hs.hotkey.bind({"cmd", "ctrl"}, "I", moveWindowToTopCenter)
hs.hotkey.bind({"cmd", "ctrl"}, "O", moveWindowToTopRight)

hs.hotkey.bind({"cmd", "ctrl"}, "J", moveWindowToLeftCenter)
hs.hotkey.bind({"cmd", "ctrl"}, "K", moveWindowToCenter)
hs.hotkey.bind({"cmd", "ctrl"}, "L", moveWindowToRightCenter)

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
