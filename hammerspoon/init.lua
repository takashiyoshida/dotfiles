-- Return a rect that allows the focused window to move to one of the screen corners
function getScreenCornerRectForFocusedWindow(location)
    local frame = hs.screen.mainScreen():frame()
    local fullFrame = hs.screen.mainScreen():fullFrame()
    local window = hs.window.focusedWindow()
    local size = window:size()

    if location == "TOP_LEFT" then
        -- top left
        return hs.geometry.rect(frame.x, frame.y, size.w, size.h)
    elseif location == "TOP_RIGHT" then
        -- top right
        return hs.geometry.rect(fullFrame.w - size.w, frame.y, size.w, size.h)
    elseif location == "BOTTOM_LEFT" then
        -- bottom left
        return hs.geometry.rect(frame.x, fullFrame.h - size.h, size.w, size.h)
    elseif location == "BOTTOM_RIGHT" then
        -- bottom right
        return hs.geometry.rect(fullFrame.w - size.w, fullFrame.h - size.h,
                                size.w, size.h)
    end
end

-- Move the current window to the top left corner
function moveWindowToTopLeft()
    local rect = getScreenCornerRectForFocusedWindow("TOP_LEFT")
    hs.window.focusedWindow():move(rect)
end
hs.hotkey.bind({"cmd", "ctrl"}, "U", moveWindowToTopLeft)

function moveWindowToTopRight()
    local rect = getScreenCornerRectForFocusedWindow("TOP_RIGHT")
    hs.window.focusedWindow():move(rect)
end
hs.hotkey.bind({"cmd", "ctrl"}, "O", moveWindowToTopRight)

function moveWindowToBottomLeft()
    local rect = getScreenCornerRectForFocusedWindow("BOTTOM_LEFT")
    hs.window.focusedWindow():move(rect)
end
hs.hotkey.bind({"cmd", "ctrl"}, "J", moveWindowToBottomLeft)

function moveWindowToBottomRight()
    local rect = getScreenCornerRectForFocusedWindow("BOTTOM_RIGHT")
    hs.window.focusedWindow():move(rect)
end
hs.hotkey.bind({"cmd", "ctrl"}, "L", moveWindowToBottomRight)

function applicationWatcher(appName, eventType, appObject)
    print('appName = ' .. appName)
    print('eventType = ' .. eventType)
    if (eventType == hs.application.watcher.launching) then
        print('launching') -- 0
    elseif (eventType == hs.application.watcher.launched) then
        print('launched') -- 1
    elseif (eventType == hs.application.watcher.terminated) then
        print('terminated') -- 2
    elseif (eventType == hs.application.watcher.hidden) then
        print('hidden') -- 3
    elseif (eventType == hs.application.watcher.unhidden) then
        print('unhidden') -- 4
    elseif (eventType == hs.application.watcher.activated) then
        print('activated') -- 5
    elseif (eventType == hs.application.watcher.deactivated) then
        print('deactivated') -- 6
    end

	if (eventType == hs.application.watcher.activated) then
		if (appName == 'Finder') then
		   -- Bring all Finder windows to forward when one gets activated
			appObject:selectMenuItem({"Window", "Bring All to Front"})
		elseif(appName == 'Fantastical') then
		    -- Switch to Fantastical 2 and open its window
		    -- Without this, Fantastical becomes active with no window in
		    -- a different space
		    appObject:selectMenuItem({"Window", "Full Calendar Window"})
		end
	end
end

local appWatcher = hs.application.watcher.new(applicationWatcher)
appWatcher:start()

-- Move the current window to the center of the screen
function center_window()
    local window = hs.window.focusedWindow()
    window:centerOnScreen()
end
hs.hotkey.bind({'cmd', 'alt', 'ctrl'}, 'c', center_window)

-- Gather all windows from the frontmost application at the center of the screen
function gather_windows()
	local app = hs.application.frontmostApplication()
	local windows = app:allWindows()
	for i, win in ipairs(windows) do
		win:centerOnScreen()
	end
end
hs.hotkey.bind({'cmd', 'alt', 'ctrl'}, 'g', gather_windows)

-- Extend the height of the current window to the bottom of the screen
function extend_window_vertically()
    local win = hs.application.frontmostApplication():mainWindow()
    local size = win:size()
    -- frame.w is the width of the window (we need to keep this)
    local screenFrame = hs.screen.mainScreen():frame()
    size.h = screenFrame.h
    win:setSize(size)
end
hs.hotkey.bind({'cmd', 'alt', 'ctrl'}, 'v', extend_window_vertically)

-- Cascade all windows of the current window
-- TODO: Come up with a better algorithm for arranging windows
-- FIXME: Windows become smaller and smaller as you use this
function cascade_windows()
    local offsetX, offsetY = 25, 25
    local f = hs.screen.mainScreen():frame()
    local app = hs.application.frontmostApplication()
    for i, win in ipairs(app:allWindows()) do
        hs.printf("i: %d", i)
        local size = win:size()
        win:move(hs.geometry.rect(f.x + ((i - 1) * offsetX), f.y + ((i - 1) * offsetY), size.w, size.h - ((i - 1) * offsetY)))
        win:focus()
    end
end
hs.hotkey.bind({'cmd', 'alt', 'ctrl'}, 'space', cascade_windows)
