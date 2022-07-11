require "window"

-- Offset to ensure that window is not covered by the SwitchGlass application switcher
SWITCHGLASS_OFFSET_X = 43
-- iTerm2 window width when it shows 80 columns (this will depend on your iTerm2 profile)
ITERM2_WINDOW_WIDTH = 665


--[[
printFocusedWindowScreen()
]]
function printFocusedWindowScreen()
    local frame = hs.window.focusedWindow():screen():frame()
    local fullFrame = hs.window.focusedWindow():screen():fullFrame()

    print("frame    : " .. frame.x, frame.y, frame.w, frame.h)
    print("fullFrame: " .. fullFrame.x, fullFrame.y, fullFrame.w, fullFrame.h)
end


--[[
moveWindowToTopLeft
]]
function moveWindowToTopLeft()
    print("moveWindowToTopLeft")
    print("Moving the current window to the top left corner of the current screen")

    local screenFrame = hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    windowFrame.x = screenFrame.x
    windowFrame.y = screenFrame.y

    print("windowFrame: " .. windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)
    hs.window.focusedWindow():move(windowFrame)
end
hs.hotkey.bind({"cmd", "ctrl"}, "U", moveWindowToTopLeft)


--[[
moveWindowToTopRight
]]
function moveWindowToTopRight()
    print("Moving the current window to the top right corner of the current screen")

    local screenFrame = hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    windowFrame.x = screenFrame.x + (screenFrame.w - SWITCHGLASS_OFFSET_X) - windowFrame.w
    windowFrame.y = screenFrame.y

    print("windowFrame: " .. windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)
    hs.window.focusedWindow():move(windowFrame)
end
hs.hotkey.bind({"cmd", "ctrl"}, "O", moveWindowToTopRight)


--[[
moveWindowToBottomLeft
]]
function moveWindowToBottomLeft()
    print("Moving the current window to the bottom left corner of the current screen")

    local screenFullFrame = hs.window.focusedWindow():screen():fullFrame()
    local screenFrame = hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    windowFrame.x = screenFrame.x
    windowFrame.y = screenFullFrame.h - windowFrame.h

    print("windowFrame: " .. windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)
    hs.window.focusedWindow():move(windowFrame)
end
hs.hotkey.bind({"cmd", "ctrl"}, "M", moveWindowToBottomLeft)


--[[
moveWindowToBottomRight
]]
function moveWindowToBottomRight()
    print("Moving the current window to the bottom right corner of the current screen")

    local screenFullFrame = hs.window.focusedWindow():screen():fullFrame()
    local windowFrame = hs.window.focusedWindow():frame()

    windowFrame.x = screenFullFrame.x + (screenFullFrame.w - SWITCHGLASS_OFFSET_X) - windowFrame.w
    windowFrame.y = screenFullFrame.h - windowFrame.h

    print("windowFrame: " .. windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)
    hs.window.focusedWindow():move(windowFrame)
end
hs.hotkey.bind({"cmd", "ctrl"}, ".", moveWindowToBottomRight)


--[[
moveWindowToCenter
]]
function center_window()
    print("Moving the current window to the center of the main screen ...")

    local appName = hs.application.frontmostApplication():name()
    if appName == "Spark" then
        local screenFrame = hs.window.focusedWindow():screen():frame()
        local windowFrame = hs.window.focusedWindow():frame()

        if screenFrame.x < 0 then
            windowFrame.x = (screenFrame.x / 2) - (windowFrame.w / 2)
        else
            windowFrame.x = (screenFrame.w / 2) - (windowFrame.w / 2)
        end

        windowFrame.y = screenFrame.y + (screenFrame.h - windowFrame.h) / 2
        hs.window.focusedWindow():move(windowFrame)
    else
        local window = hs.window.focusedWindow()
        window:centerOnScreen()
    end
end
hs.hotkey.bind({"cmd", "ctrl"}, "K", center_window)


--[[
moveWindowToLeftCenter
]]
function moveWindowToLeftCenter()
    print("Moving the current window to the left center of the current screen")

    local screenFrame = hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    windowFrame.x = screenFrame.x
    windowFrame.y = screenFrame.y + (screenFrame.h - windowFrame.h) / 2

    print("windowFrame: " .. windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)
    hs.window.focusedWindow():move(windowFrame)
end
hs.hotkey.bind({"cmd", "ctrl"}, "J", moveWindowToLeftCenter)


--[[
moveWindowToRightCenter
]]
function moveWindowToRightCenter()
    print("Moving the current window to the right center of the current screen")

    local screenFrame = hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    windowFrame.x = screenFrame.x + (screenFrame.w - SWITCHGLASS_OFFSET_X) - windowFrame.w
    windowFrame.y = screenFrame.y + (screenFrame.h - windowFrame.h) / 2

    print("windowFrame: " .. windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)
    hs.window.focusedWindow():move(windowFrame)
end
hs.hotkey.bind({"cmd", "ctrl"}, "L", moveWindowToRightCenter)


--[[
moveWindowToTopCenter
]]
function moveWindowToTopCenter()
    print("Moving the current window to the top center of the current screen")

    local screenFrame = hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    print("screenFrame: " .. screenFrame.x, screenFrame.y, screenFrame.w, screenFrame.h)

    if screenFrame.x < 0 then
        windowFrame.x = (screenFrame.x / 2) - (windowFrame.w / 2)
    else
        windowFrame.x = (screenFrame.w / 2) - (windowFrame.w / 2)
    end
    windowFrame.y = screenFrame.y

    print("windowFrame: " .. windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)
    hs.window.focusedWindow():move(windowFrame)
end
hs.hotkey.bind({"cmd", "ctrl"}, "I", moveWindowToTopCenter)


--[[
moveWindowToBottomCenter
]]
function moveWindowToBottomCenter()
    print("Moving the current window to the bottom center of the current screen")

    local screenFullFrame = hs.window.focusedWindow():screen():fullFrame()
    local screenFrame = hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    if screenFrame.x < 0 then
        windowFrame.x = (screenFrame.x / 2) - (windowFrame.w / 2)
    else
        windowFrame.x = (screenFrame.w / 2) - (windowFrame.w / 2)
    end
    windowFrame.y = screenFullFrame.h - windowFrame.h

    print("windowFrame: " .. windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)
    hs.window.focusedWindow():move(windowFrame)
end
hs.hotkey.bind({"cmd", "ctrl"}, ",", moveWindowToBottomCenter)


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
hs.hotkey.bind({"ctrl", "alt"}, "U", resizeWindowToTopLeftThird)


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
hs.hotkey.bind({"ctrl", "alt"}, "I", resizeWindowToTopCenterThird)


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
hs.hotkey.bind({"ctrl", "alt"}, "O", resizeWindowToTopRightThird)


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
hs.hotkey.bind({"ctrl", "alt"}, "M", resizeWindowToBottomLeftThird)


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
hs.hotkey.bind({"ctrl", "alt"}, ",", resizeWindowToBottomCenterThird)


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
hs.hotkey.bind({"ctrl", "alt"}, ".", resizeWindowToBottomRightThird)


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
hs.hotkey.bind({"cmd", "ctrl", "shift"}, "L", moveWindowToOneScreenEast)


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
hs.hotkey.bind({"cmd", "ctrl", "shift"}, "J", moveWindowToOneScreenWest)

function maximizeWindow()
    local frame = hs.screen.mainScreen():frame()
    local fullFrame = hs.screen.mainScreen():fullFrame()

    print("Maximizing the current window ...")
    print("frame: " .. frame.x, frame.y, frame.w, frame.h)
    print("fullFrame: " .. fullFrame.x, fullFrame.y, fullFrame.w, fullFrame.h)

    -- Ensure that the maximized window is not covered by the SwitchGlass application switcher
    local rect = hs.geometry.rect(frame.x, frame.y, frame.w - SWITCHGLASS_OFFSET_X, frame.h)
    hs.window.focusedWindow():move(rect)
end
hs.hotkey.bind({"cmd", "ctrl"}, "Z", maximizeWindow)

-- Move Twitterrific windows to the top-right corner of the screen
function foobar()
    local app = hs.application.applicationsForBundleID("com.iconfactory.Twitterrific5")
    app[1]:activate()

    local offset = 0
    for i, window in ipairs(app[1]:visibleWindows()) do
        hs.printf("Window %d: title: %s standard: %s", i, window:title(), window:isStandard())
        if window:isStandard() then
            -- Move the window to top right corner of the screen
            local screenFrame = window:screen():frame()
            local windowFrame = window:frame()

            windowFrame.x = screenFrame.x + (screenFrame.w - SWITCHGLASS_OFFSET_X) - windowFrame.w
            windowFrame.y = screenFrame.y
            -- windowFrame.x needs to be adjusted
            windowFrame.x = windowFrame.x - (windowFrame.w * (i - 1))
            print("windowFrame: " .. windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)
            window:move(windowFrame)
        end
    end
end
hs.hotkey.bind({"cmd", "ctrl"}, "T", foobar)


function applicationWatcher(appName, eventType, appObject)
    print("Calling applicationWatcher ...")
    print("appName = " .. appName)
    print("eventType = " .. eventType)
    if (eventType == hs.application.watcher.launching) then
        print("launching") -- 0
    elseif (eventType == hs.application.watcher.launched) then
        print("launched") -- 1
    elseif (eventType == hs.application.watcher.terminated) then
        print("terminated") -- 2
    elseif (eventType == hs.application.watcher.hidden) then
        print("hidden") -- 3
    elseif (eventType == hs.application.watcher.unhidden) then
        print("unhidden") -- 4
    elseif (eventType == hs.application.watcher.activated) then
        print("activated") -- 5
    elseif (eventType == hs.application.watcher.deactivated) then
        print("deactivated") -- 6
    end

    if (eventType == hs.application.watcher.activated) then
        if (appName == "Finder") then
            -- Bring all Finder windows to forward when one gets activated
            print("Switching to Finder ...")
            appObject:selectMenuItem({"Window", "Bring All to Front"})
        elseif (appName == "Fantastical") then
            -- Switch to Fantastical 2 and open its window
            -- Without this, Fantastical becomes active with no window in
            -- a different space
            print("Switching to Fantastical ...")
            appObject:selectMenuItem({"Window", "Full Calendar Window"})
        end
    end
end

local appWatcher = hs.application.watcher.new(applicationWatcher)
appWatcher:start()

-- Gather all windows from the frontmost application at the center of the screen
function gather_windows()
    local app = hs.application.frontmostApplication()
    local windows = app:allWindows()
    for i, win in ipairs(windows) do
        win:centerOnScreen()
    end
end
-- hs.hotkey.bind({'cmd', 'alt', 'ctrl'}, 'g', gather_windows)

-- Extend the height of the current window to the bottom of the screen
function extend_window_vertically()
    print("Extending window vertically ...")
    local win = hs.application.frontmostApplication():mainWindow()
    local size = win:size()
    -- frame.w is the width of the window (we need to keep this)
    local screenFrame = hs.screen.mainScreen():frame()
    size.h = screenFrame.h
    win:setSize(size)
end
hs.hotkey.bind({"cmd", "alt", "ctrl"}, "v", extend_window_vertically)

-- Cascade all windows of the current application
function cascade_windows()
    -- the current target behavior is:
    -- move the first window to the top left corner
    -- adjust the location of the next window by moving it down and right
    -- don't adjust the window size (yet)

    print("Cascading all windows ...")

    local app = hs.application.frontmostApplication()
    local mainFrame = hs.screen.mainScreen():frame()

    local offsetX, offsetY = 28, 28
    local n = 1

    for i, window in ipairs(app:allWindows()) do
        hs.printf(
            "Window %d: title: %s; visible: %s; standard: %s",
            i,
            window:title(),
            window:isVisible(),
            window:isStandard()
        )
        hs.printf("      size: %d, %d", window:size().w, window:size().h)

        if not window:isStandard() or window:title() == "" then
            hs.printf("Window %s is not a standard window or has no titles; Ignoring ...", window:title())
            -- why did I decide to move the window at the center the screen?
            window:centerOnScreen()
        else
            local newX = mainFrame.x + ((n - 1) * offsetX)
            local newY = mainFrame.y + ((n - 1) * offsetY)

            -- right now, the height of the window is not adjusted even when
            -- the window is moved down
            -- the window's height needs to be adjusted so that the bottom of the window
            -- can be seen on the screen.

            local newW = window:size().w
            local newH = window:size().h - ((n - 1) * offsetY)

            hs.printf("Moving window %d to (%d, %d, %d, %d) ...", n, newX, newY, newW, newH)
            window:move(hs.geometry.rect(newX, newY, newW, newH))
            n = n + 1
        end
    end
end
hs.hotkey.bind({"cmd", "alt", "ctrl"}, "space", cascade_windows)

function resize_browser_window_for_google()
    print("Resizing browser window for Google search page ...")
    if
        (hs.application.frontmostApplication():name() == "Safari") or
            (hs.application.frontmostApplication():name() == "Google Chrome") or
            (hs.application.frontmostApplication():name() == "Brave")
     then
        local win = hs.application.frontmostApplication():mainWindow()
        local frame = win:frame()
        print("frame: " .. frame.x, frame.y, frame.w, frame.h)
        if (frame.w < 1200) then
            local screen = hs.screen.mainScreen():fullFrame()
            if ((frame.x + 1200) > screen.w) then
                -- Move the window to the left
                frame.x = screen.w - 1200
            end
        end
        frame.w = 1200
        win:move(frame)
    end
end
hs.hotkey.bind({"cmd", "alt", "ctrl"}, "g", resize_browser_window_for_google)


function resize_browser_window_for_iterm()
    print("Resizing browser window for iTerm ...")
    if
        (hs.application.frontmostApplication():name() == "Safari") or
            (hs.application.frontmostApplication():name() == "Google Chrome") or
            (hs.application.frontmostApplication():name() == "Brave")
     then
        moveWindowToTopLeft()
        local win = hs.application.frontmostApplication():mainWindow()
        local frame = win:frame()
        print("frame: " .. frame.x, frame.y, frame.w, frame.h)
        frame.w = 980
        win:move(frame)
    end
end
-- hs.hotkey.bind({"cmd", "alt", "ctrl"}, "t", resize_browser_window_for_iterm)

function test()
    local frame = hs.screen.mainScreen():frame()
    local fullFrame = hs.screen.mainScreen():fullFrame()

    local rect = hs.geometry.rect(frame.x, frame.y, 1258.5, 707.5)
    hs.window.focusedWindow():move(rect)
end
hs.hotkey.bind({"cmd", "ctrl"}, "R", test)


