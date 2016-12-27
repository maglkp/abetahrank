open System

// empty hex, red and blue stones
let R = 'R'
let B = 'B'
let E = '-'

// read input grid, player and board size
let (grid: string list, player: char, N: int) = 
    let player = Console.ReadLine().[0]
    let size = Int32.Parse(Console.ReadLine())    
    let board = List.init size (fun _ -> Console.ReadLine())    
    board, player, size

let printGridList grid =
    grid |> List.iter (fun line -> printfn "%s" line)
    
let insert (grid:string list) (element:char) (r:int) (c:int) =
    let insert (line:string) char pos =
        line.Substring(0, pos) + char.ToString() + line.Substring(pos + 1)      
    let updatedLine = insert grid.[r] element c
    grid.[0..r-1] @ (updatedLine :: grid.[r+1..N-1])

printGridList (insert grid '@' 10 10)