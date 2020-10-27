SetKeyDelay, 125

GoalNumber := 1
GoodGoals := ""

Gui, +LastFound -Caption +AlwaysOnTop
Gui, Add, Text, , Good goal?
Gui, Add, Button, xm gYes w40, Yes
Gui, Add, Button, x+10 gNo w40, No



ResetReplay()
{
    BlockInput, MouseMove
    MouseMove, 5,5
    Send {Escape}
    Send {Down}
    Send {Enter}
    Sleep, 200
    Send {Enter}
    BlockInput, MouseMoveOff
    return 0
}

SetCamera()
{
    Click, right
    Click, right
    Click, right
    Click, right
    Click, right
}

GetNextKeyframeInInterval(Keyframe)
{
    Interval := 5
    Multiplier := 0.03
    NumIntervals := Floor((Keyframe * Multiplier - 1) / Interval)
    return NumIntervals
    MsgBox, 4,, %NumIntervals%
}

GetLineFromFile(LineNum, Filename)
{
    FileReadLine, File, Filename, LineNum
    return File
}

GetGameNumber() 
{
    FileReadLine, GameNumber, C:\Users\stream\Documents\My Games\Rocket League\TAGame\Demos\active.txt, 2
    return GameNumber
}

GetVideoNumber() 
{
    FileReadLine, VideoNumber, C:\Users\stream\Documents\My Games\Rocket League\TAGame\Demos\active.txt, 1
    return VideoNumber
}

GetNextGoalKeyframe() {
    global GoalNumber
    global GoodGoals
    VideoNumber := GetVideoNumber()
    GameNumber := GetGameNumber()
    LineNumber := GoalNumber + 1
    Line2 := 1
    Path := "C:\Users\stream\Documents\My Games\Rocket League\TAGame\Demos\" VideoNumber "\Game" GameNumber ".txt"
    ;Loop, read, %Path%
    ;{
        
    ;    Loop, parse, A_LoopReadLine, %A_Tab%
    ;    {
    ;        if(Line2 != 1) 
     ;       {
    ;            MsgBox, Frame: %A_LoopField% Line: %Line2% %GoalNumber%
    ;        }
    ;        Line2 += 1
    ;    }
    ;}
    FileReadLine, Keyframe, %Path%, %LineNumber%
    ToolTip, %Keyframe%
    if (Keyframe < 1) ;Break if no goals left
    {
        if WinExist("ahk_exe Code.exe")
        {
            WinActivate, ahk_exe Code.exe
            Click, 381, 1057
            TrimGoals := LTrim(GoodGoals)
            Send,%TrimGoals%{Enter}
            WinActivate, Rocket League
        }
        Reload
        Sleep, 1000
        MsgBox, Something went wrong reloading the script
    }
    return Keyframe
}

NextGoal()
{
    global GoalNumber
    NextFrame := GetNextGoalKeyframe()
    ToolTip, %NextFrame%
    ResetReplay()
    FastForwards := GetNextKeyframeInInterval(NextFrame) ; 410 is roughly 8 seconds
    Sleep, 2000
    SetCamera()
    ToolTip, %FastForwards%
    Loop, %FastForwards%
    {
        Send {Right}
    }
    GoalNumber += 1
    Gui, Show, x5 y5
    MouseMove, 5,5
}



Yes()
{
    Gui, Hide   ;hides the window
    WinActivate, Rocket League
    global GoalNumber
    global GoodGoals
    GoalAdjust := GoalNumber - 1
    GoodGoals .= " " GoalAdjust
    NextGoal()
}

No()
{
    Gui, Hide
    NextGoal()
}


WatchAllGoals() 
{
    NextGoal()
}

#IfWinActive, Rocket League
{
    w::ResetReplay()

    s::SetCamera()
    
    d::NextGoal()

    e::GetNextGoalKeyframe()

    x::WatchAllGoals()

    y::Yes()

    n::No()

    q::
    

    return
}