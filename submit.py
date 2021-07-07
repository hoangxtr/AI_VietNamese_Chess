import copy


AI_TEAM=None
AI_BOARD = None

neighborDict = {}
adjacentDict = {}
neighborPosL = []
adjacentPosL = []
for r in range(5):
    for c in range(5):
        neighborPosL = [(r, c - 1), (r, c + 1), (r - 1, c), (r + 1, c), (r - 1, c - 1), (r + 1, c + 1), (r - 1, c + 1), (r + 1, c - 1)]
        if (r % 2 == 0 and c % 2 != 0) or (r % 2 != 0 and c % 2 == 0):
            adjacentPosL = [(r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)]
            adjacentPosL = list( filter(lambda x: (0 <= x[0] < 5) and (0 <= x[1] < 5), adjacentPosL) )
            neighborPosL = list( filter(lambda x: (0 <= x[0] < 5) and (0 <= x[1] < 5), neighborPosL) )
            neighborDict[r*5 + c] = neighborPosL
            adjacentDict[r*5 + c] = adjacentPosL
        else:
            adjacentPosL = neighborPosL = list( filter(lambda x: (0 <= x[0] < 5) and (0 <= x[1] < 5), neighborPosL) )
            adjacentDict[r*5 + c] = neighborDict[r*5 + c] = neighborPosL
        
        adjacentPosL = neighborPosL = []

def cmp_board(board1, board2):
    for i in range(25):
        if board1[i//5][i%5] != board2[i//5][i%5]:
            return False
    return True

def my_move(board, fromPos, toPos):
    board = copy.deepcopy(board)
    if board[ fromPos[0] ][ fromPos[1] ] == 0 or board[ toPos[0] ][ toPos[1] ] != 0:
        return None
    board[ toPos[0] ][ toPos[1] ] = board[ fromPos[0] ][ fromPos[1] ]
    board[ fromPos[0] ][ fromPos[1] ] = 0
    return board

def new_ganh(board, nearst_move):
    '''
    check enemy team is "ganh" or not 
    co the bi loi
    '''
    board = copy.deepcopy(board)
    nearst_move = nearst_move[0] * 5 + nearst_move[1] 
    def process(board, pos):
        temp_board = copy.deepcopy(board)
        board = []
        for i in range(5):
            for j in range(5):
                board.append(temp_board[i][j])
        if pos % 2 == 0:
            if 1 <= pos // 5 <= 3 and 1 <= pos % 5 <= 3:
                if board[pos] * -2 == board[pos-6] + board[pos+6]:
                    board[pos-6] = board[pos]
                    board[pos+6] = board[pos]
                if board[pos] * -2 == board[pos-4] + board[pos+4]:
                    board[pos-4] = board[pos]
                    board[pos+4] = board[pos]
        if pos-1 >= 0 and pos + 1 <= 24 and (pos-1) % 5 < (pos+1) % 5:
            if board[pos] * -2 == board[pos-1] + board[pos+1]:
                board[pos-1] = board[pos]
                board[pos+1] = board[pos]
        if pos-5 >= 0 and pos + 5 <= 24 and (pos-5) // 5 < (pos+5) // 5:
            if board[pos] * -2 == board[pos-5] + board[pos+5]:
                board[pos-5] = board[pos]
                board[pos+5] = board[pos]
        for i in range(5):
            for j in range(5):
                temp_board[i][j] = board[i*5+j]
        return temp_board

    board = process(board, nearst_move)
    return board

def eveluate(board):
    count = 0
    for i in range(5):
        for j in range(5):
            if board[i][j] == AI_TEAM:
                count += 1
    if count == 0:
        print('Player won')
        return -30

    if count == 16:
        print('AI won')
        return 30
    
    return count

def minimax(board, a, b, dept, myTurn):
    temp_board = None
    if dept == 0:
        return eveluate(board)
    stop = False
    
    if myTurn:
        team_pos = []
        for i in range(5):
            for j in range(5):
                if board[i][j] == AI_TEAM:
                    team_pos.append((i,j))
        # team_pos = np.where(board == AI_TEAM)
        for pos in team_pos:
            neighbors = adjacentDict[pos[0]*5 + pos[1]]
            for neighbor in neighbors:
                if board[ neighbor[0] ][ neighbor[1] ] != 0:
                    continue
                temp_board = copy.deepcopy(board)
                temp_board = my_move(temp_board, pos, neighbor)
                temp_board = postprocess_move(temp_board, pos, neighbor, AI_TEAM)
                temp = minimax(temp_board, a, b, dept-1, False)
                a = max(a, temp)
                if a >= b:
                    stop = True
                    break
            if stop:
                break
        return a
    else:
        team_pos = []
        for i in range(5):
            for j in range(5):
                if board[i][j] == -1 * AI_TEAM:
                    team_pos.append((i,j))
        # team_pos = np.where(board == -1 * AI_TEAM)
        for pos in team_pos:
            neighbors = adjacentDict[pos[0]*5 + pos[1]]
            for neighbor in neighbors:
                if board[ neighbor[0] ][ neighbor[1] ] != 0:
                    continue
                temp_board = copy.deepcopy(board)
                temp_board = my_move(temp_board, pos, neighbor)
                temp_board = postprocess_move(temp_board, pos, neighbor, -1*AI_TEAM)
                temp = minimax(temp_board, a, b, dept-1, True)
                b = min(b, temp)
                if a >= b:
                    stop = True
                    break
            if stop:
                break
        return b

def traverse_CHET(startPos, currColor, oppColor, state, q = []):
    
    state[ startPos[0] ][ startPos[1] ] = currColor
    q.append(startPos)
    for x in adjacentDict[ startPos[0]*5 + startPos[1] ]:
        if (state[ x[0] ][ x[1] ] == 0) or ( state[ x[0] ][ x[1] ] == oppColor and ( not traverse_CHET(x, currColor, oppColor, state, q) ) ):
            while(q[-1] != startPos):
                state[ q[-1][0] ][ q[-1][1] ] = oppColor
                q.pop()
            state[ startPos[0] ][ startPos[1] ] = oppColor
            q.pop()
            return False
            
    return True

def postprocess_move(board, fromPos, toPos, team):
    '''
    fromPos: Vị trí cũ
    toPos: vị trí mới
    team: team vừa di chuyển
    '''
    neighbors = adjacentDict[toPos[0]*5+toPos[1]]
    board = copy.deepcopy(board)
    board = new_ganh(board, toPos)
    for neighbor in neighbors:
        if board[ neighbor[0] ][ neighbor[1] ] == team*-1:
            traverse_CHET(neighbor, team, team*-1, board)
   
    return board

def get_next_move(board):
    score = 0
    max_score=-40
    nextMove = None

    team_pos = []
    for i in range(5):
        for j in range(5):
            if board[i][j] == AI_TEAM:
                team_pos.append((i,j))
    # team_pos = np.where(board == AI_TEAM)
    for pos in team_pos:
        neighbors = adjacentDict[pos[0]*5 + pos[1]]
        for neighbor in neighbors:
            if board[ neighbor[0] ][ neighbor[1] ] != 0:
                continue
            temp_board = copy.deepcopy(board)
            temp_board = my_move(temp_board, pos, neighbor)
            temp_board = postprocess_move(temp_board, pos, neighbor, AI_TEAM)
            score = minimax(temp_board, -30, 30, 1, False)
            # print('+++++++++++++++++++++++++++++++++++++++++++++++!')
            # print('pos: ', pos)
            # print('score: ', score)
            # print('================================================/')
            if score >= max_score:
                
                nextMove = [pos, neighbor]
                max_score = score
    print(nextMove)
    return nextMove

def process(board, player):
    global AI_TEAM
    AI_TEAM = player
    global AI_BOARD

    if AI_BOARD == None:
        AI_BOARD = board
        nextMove = get_next_move(board)
        AI_BOARD = my_move(AI_BOARD, nextMove[0], nextMove[1])
        return nextMove
    
    fromPos = None
    toPos = None
    for i in range(5):
        for j in range(5):
            if board[i][j] != AI_BOARD[i][j]:
                if AI_BOARD[i][j] == -1 * AI_TEAM and board[i][j] == 0:
                    fromPos = (i,j)
                elif AI_BOARD[i][j] == 0 and board[i][j] == -1 * AI_TEAM:
                    toPos = (i,j)
    
    # Co ganh or vay
    if eveluate(AI_BOARD) != eveluate(board):
        nextMove = get_next_move(board)
        if nextMove != None:
            AI_BOARD = my_move(board, nextMove[0], nextMove[1])
            AI_BOARD = postprocess_move(AI_BOARD, nextMove[0], nextMove[1], AI_TEAM)
        return nextMove
    
    neighbors_can_move = [] # Luu cac neighbor co the di chuyen khi dinh bay
    # Khong ganh or vay
    neighbors = adjacentDict[fromPos[0]*5+fromPos[1]]
    for neighbor in neighbors:
        if board[ neighbor[0] ][ neighbor[1] ] != AI_TEAM:
            continue
        temp_board = copy.deepcopy(board)
        temp_board = my_move(temp_board, neighbor, fromPos)
        if not cmp_board(new_ganh(temp_board, fromPos), temp_board): # co the ganh duoc
            neighbors_can_move.append(neighbor)
    
    if len(neighbors_can_move) == 0:
        nextMove = get_next_move(board)
        if nextMove != None:
            AI_BOARD = my_move(board, nextMove[0], nextMove[1])
            AI_BOARD = postprocess_move(AI_BOARD, nextMove[0], nextMove[1], AI_TEAM)
        return nextMove
    
    else:
        # print('Co bay')
        nextMove = (neighbors_can_move[0],fromPos)
        AI_BOARD = my_move(board, nextMove[0], nextMove[1])
        AI_BOARD = postprocess_move(AI_BOARD, nextMove[0], nextMove[1], AI_TEAM)
        return nextMove
    
def move(board, player, remain_time): # khong sua ten ham nay
    return process(board, player)