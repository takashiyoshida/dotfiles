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

hs.hotkey.bind({"cmd", "ctrl"}, "Left", hs.fnutils.partial(winresize, "left"))
hs.hotkey.bind({"cmd", "ctrl"}, "Right", hs.fnutils.partial(winresize, "right"))
hs.hotkey.bind({"cmd", "ctrl"}, "Up", hs.fnutils.partial(winresize, "up"))
hs.hotkey.bind({"cmd", "ctrl"}, "Down", hs.fnutils.partial(winresize, "down"))
hs.hotkey.bind({"cmd", "ctrl", "alt"}, "F", hs.fnutils.partial(winresize, "max"))

hs.hotkey.bind({"ctrl", "alt"}, "Left", left_third)
hs.hotkey.bind({"ctrl", "alt"}, "Right", right_third)
hs.hotkey.bind({"ctrl", "alt"}, "Up", up_third)
hs.hotkey.bind({"ctrl", "alt"}, "Down", down_third)
