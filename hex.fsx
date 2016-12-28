open System

// empty hex, red and blue stones
let R = 'R'
let B = 'B'
let E = '-'
let VISITED = 'X'

// read input grid, player and board size
let (grid: string list, player: char, N: int) = 
    let player = Console.ReadLine().[0]
    let size = Int32.Parse(Console.ReadLine())    
    let board = List.init size (fun _ -> Console.ReadLine())    
    board, player, size

let printGridList grid =
    grid |> List.iter (fun line -> printfn "%s" line)
    
let insert (grid:string list) (element:char) (r:int, c:int) =
    let insertInStr (line:string) char pos =
        line.Substring(0, pos) + char.ToString() + line.Substring(pos + 1) 
    let updatedLine = insertInStr grid.[r] element c
    grid.[0..r-1] @ (updatedLine :: grid.[r+1..N-1])

let neighbours (grid:string list) r c cellValue = 
    let rMin, rMax = max (r-1) 0, min (r+1) (N-1)
    let cMin, cMax = max (c-1) 0, min (c+1) (N-1)
    seq {
        for i = rMin to rMax do
            for j = cMin to cMax do
                // exclude lower right and upper left corner
                if (i, j) <> ((r-1), (c-1)) && (i, j) <> ((r+1), (c+1)) && grid.[i].[j] = cellValue then
                    yield (i, j)
    }

let rec visit (grid:string list) (r, c) isGoal color =
    if isGoal r c grid then
        true
    else
        let updatedGrid = insert grid VISITED (r, c)
        Seq.exists (fun nb -> (visit updatedGrid nb isGoal color)) (neighbours updatedGrid r c color)
        
let isWonByBlue (grid:string list) =            
    let isGoal r c (grid:string list) = grid.[r].[c] = B && c = N-1
    [0..N-1] |> List.exists (fun r -> grid.[r].[0] = B && (visit grid (r, 0) isGoal B))

let isWonByRed (grid:string list) =            
    let isGoal r c (grid:string list) = grid.[r].[c] = R && r = N-1
    [0..N-1] |> List.exists (fun c -> grid.[0].[c] = R && (visit grid (0, c) isGoal R))
    

//let rec fa() = 
    //let uu = fb()
    //3
//and fb() =
    //let tt = fa()
    //8

let rec maxValue board a b =
    let rec bestAction moves bestMove bestv a b = 
        match moves with
        | m::ms ->                 
                let minValueForNode = minValue (insert board B m) a b
                let updatedV, updatedMove = 
                    if minValueForNode >= bestv then
                        minValueForNode, m
                    else
                        bestv, bestMove
                if updatedV >= b then 
                    updatedV, updatedMove 
                else 
                   bestAction ms updatedMove updatedV (max a updatedV) b
        | [] -> bestv, bestMove

    let blueWin = isWonByBlue board
    let redWin = isWonByRed board
    if blueWin then 1, (0, 0)
    else if redWin then -1, (0, 0)
    else
        let v = Int32.MinValue        
        v, (0,0)

and minValue board a b =
    let tt = maxValue board a b
    0


//printGridList (insert grid '@' 10 10)
//printfn "%A" (isWonByRed grid)
//printfn "%A" (isWonByBlue grid)

printfn "\ndone..." 

