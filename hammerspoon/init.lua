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

function test()
    local frame = hs.screen.mainScreen():frame()
    local fullFrame = hs.screen.mainScreen():fullFrame()

    local rect = hs.geometry.rect(frame.x, frame.y, 1258.5, 707.5)
    hs.window.focusedWindow():move(rect)
end


hs.hotkey.bind({"cmd", "ctrl"}, "T", foobar)
-- hs.hotkey.bind({'cmd', 'alt', 'ctrl'}, 'g', gather_windows)
hs.hotkey.bind({"cmd", "alt", "ctrl"}, "v", extend_window_vertically)
hs.hotkey.bind({"cmd", "alt", "ctrl"}, "space", cascade_windows)
hs.hotkey.bind({"cmd", "alt", "ctrl"}, "g", resize_browser_window_for_google)
-- hs.hotkey.bind({"cmd", "alt", "ctrl"}, "t", resize_browser_window_for_iterm)
hs.hotkey.bind({"cmd", "ctrl"}, "R", test)
