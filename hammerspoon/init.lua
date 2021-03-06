-- Offset to ensure that window is not covered by the SwitchGlass application switcher
SWITCHGLASS_OFFSET_X = 43

function printFocusedWindowScreen()
    local frame = hs.window.focusedWindow():screen():frame()
    local fullFrame = hs.window.focusedWindow():screen():fullFrame()

    print("frame    : " .. frame.x, frame.y, frame.w, frame.h)
    print("fullFrame: " .. fullFrame.x, fullFrame.y, fullFrame.w, fullFrame.h)
end

function moveWindowToTopLeft()
    print("Moving the current window to the top left corner ...")

    local screenFrame = hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    windowFrame.x = screenFrame.x
    windowFrame.y = screenFrame.y

    print("windowFrame: " .. windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)
    hs.window.focusedWindow():move(windowFrame)
end
hs.hotkey.bind({"cmd", "ctrl"}, "U", moveWindowToTopLeft)

function moveWindowToTopRight()
    print("Moving the current window to the top right corner ...")

    local screenFrame = hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    windowFrame.x = screenFrame.x + (screenFrame.w - SWITCHGLASS_OFFSET_X) - windowFrame.w
    windowFrame.y = screenFrame.y

    print("windowFrame: " .. windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)
    hs.window.focusedWindow():move(windowFrame)
end
hs.hotkey.bind({"cmd", "ctrl"}, "O", moveWindowToTopRight)

function moveWindowToBottomLeft()
    print("Moving the current window to the bottom left corner ...")

    local screenFullFrame = hs.window.focusedWindow():screen():fullFrame()
    local screenFrame = hs.window.focusedWindow():screen():frame()
    local windowFrame = hs.window.focusedWindow():frame()

    windowFrame.x = screenFrame.x
    windowFrame.y = screenFullFrame.h - windowFrame.h

    print("windowFrame: " .. windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)
    hs.window.focusedWindow():move(windowFrame)
end
hs.hotkey.bind({"cmd", "ctrl"}, "J", moveWindowToBottomLeft)

function moveWindowToBottomRight()
    print("Moving the current window to the bottom right corner ...")
    local screenFullFrame = hs.window.focusedWindow():screen():fullFrame()
    local windowFrame = hs.window.focusedWindow():frame()

    windowFrame.x = screenFullFrame.x + (screenFullFrame.w - SWITCHGLASS_OFFSET_X) - windowFrame.w
    windowFrame.y = screenFullFrame.h - windowFrame.h

    print("windowFrame: " .. windowFrame.x, windowFrame.y, windowFrame.w, windowFrame.h)
    hs.window.focusedWindow():move(windowFrame)
end
hs.hotkey.bind({"cmd", "ctrl"}, "L", moveWindowToBottomRight)

function moveWindowToOneScreenEast()
    hs.window.focusedWindow():moveOneScreenEast(true, true)
end
hs.hotkey.bind({"cmd", "ctrl", "shift"}, "L", moveWindowToOneScreenEast)

function moveWindowToOneScreenWest()
    hs.window.focusedWindow():moveOneScreenWest(true, true)
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

-- Move the current window to the center of the screen
function center_window()
    print("Moving the current window to the center of the main screen ...")
    local window = hs.window.focusedWindow()
    window:centerOnScreen()
end
hs.hotkey.bind({"cmd", "alt", "ctrl"}, "c", center_window)

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

    local offsetX, offsetY = 25, 25
    local n = 1

    for i, window in ipairs(app:allWindows()) do
        hs.printf(
            "Window %d: title: %s visible: %s standard: %s",
            i,
            window:title(),
            window:isVisible(),
            window:isStandard()
        )
        hs.printf("      size: %d, %d", window:size().w, window:size().h)

        if not window:isStandard() or window:title() == "" then
            hs.printf("Window % is not a standard window or has no titles; Ignoring ...")
            window:centerOnScreen()
        else
            local newX = mainFrame.x + ((n - 1) * offsetX)
            local newY = mainFrame.y + ((n - 1) * offsetY)

            hs.printf("Moving window %d to (%d, %d) ...", n, newX, newY)
            window:move(hs.geometry.rect(newX, newY, window:size().w, window:size().h))
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
hs.hotkey.bind({"cmd", "alt", "ctrl"}, "t", resize_browser_window_for_iterm)
