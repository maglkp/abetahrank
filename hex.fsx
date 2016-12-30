open System

// empty hex, red and blue stones
let R = 'R'
let B = 'B'
let E = '-'
let VISITED = 'X'
let NO_MOVE = (-1, -1)

// read input board, player and board size
let (board: string list, player: char, N: int) = 
    let player = Console.ReadLine().[0]
    let size = Int32.Parse(Console.ReadLine())    
    let board = List.init size (fun _ -> Console.ReadLine())    
    board, player, size

let printBoardList board =
    board |> List.iter (fun line -> printfn "%s" line)
    
let insert (board:string list) (element:char) (r:int, c:int) =
    let insertInStr (line:string) char pos =
        line.Substring(0, pos) + char.ToString() + line.Substring(pos + 1) 
    let updatedLine = insertInStr board.[r] element c
    board.[0..r-1] @ (updatedLine :: board.[r+1..N-1])

let neighbours (board:string list) r c cellValue = 
    let rMin, rMax = max (r-1) 0, min (r+1) (N-1)
    let cMin, cMax = max (c-1) 0, min (c+1) (N-1)
    seq {
        for i = rMin to rMax do
            for j = cMin to cMax do
                // exclude lower right and upper left corner
                if (i, j) <> ((r-1), (c-1)) && (i, j) <> ((r+1), (c+1)) && board.[i].[j] = cellValue then
                    yield (i, j)
    }

let rec visit (board:string list) (r, c) isGoal color =
    if isGoal r c board then
        true
    else
        let updatedBoard = insert board VISITED (r, c)
        Seq.exists (fun nb -> (visit updatedBoard nb isGoal color)) (neighbours updatedBoard r c color)
        
let isWonByBlue (board:string list) =
    let isGoal r c (board:string list) = board.[r].[c] = B && c = N-1
    [0..N-1] |> List.exists (fun r -> board.[r].[0] = B && (visit board (r, 0) isGoal B))

let isWonByRed (board:string list) =
    let isGoal r c (board:string list) = board.[r].[c] = R && r = N-1
    [0..N-1] |> List.exists (fun c -> board.[0].[c] = R && (visit board (0, c) isGoal R))

let getMoves (board:string list) =    
    seq {
        for i = 0 to N - 1 do
            for j i = 0 to N - 1 do
                if board.[i].[j] = E then
                    yield (i, j)
    } |> List.ofSeq

let rec maxValue board a b =
    let rec bestAction moves bestMove bestv a b = 
        match moves with
        | m::ms ->                 
                let minValueForNode = minValue (insert board B m) a b
                let updatedV, updatedMove = 
                    // update the maximal value and corresponding move
                    if minValueForNode >= bestv then
                        minValueForNode, m
                    else
                        bestv, bestMove
                if updatedV >= b then 
                    printfn "trimmed max"
                    updatedV, updatedMove 
                else 
                   bestAction ms updatedMove updatedV (max a updatedV) b
        | [] -> bestv, bestMove

    let blueWin = isWonByBlue board
    let redWin = isWonByRed board
    if blueWin then 1, NO_MOVE
    else if redWin then -1, NO_MOVE
    else
        let moves = (getMoves board)
        bestAction moves (List.head moves) Int32.MinValue a b

and minValue board a b =
    let rec bestAction moves bestMove bestv a b =
        match moves with
        | m::ms ->                 
                let maxValueForNode = fst(maxValue (insert board R m) a b)
                let updatedV, updatedMove = 
                    // update the minimal value and corresponding move
                    if maxValueForNode <= bestv then
                        maxValueForNode, m
                    else
                        bestv, bestMove
                if updatedV <= a then 
                    printfn "trimmed min"
                    updatedV 
                else 
                   bestAction ms updatedMove updatedV a (min b updatedV)
        | [] -> bestv

    let blueWin = isWonByBlue board
    let redWin = isWonByRed board
    if blueWin then 1
    else if redWin then -1
    else
        let moves = (getMoves board)
        bestAction moves (List.head moves) Int32.MaxValue a b

let absearch board = 
    maxValue board Int32.MinValue Int32.MaxValue 


//printBoardList (insert board '@' 10 10)
//printfn "%A" (isWonByRed board)
printfn "%A" (absearch board)
printfn "\ndone..." 

