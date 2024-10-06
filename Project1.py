from random import randint
board = ['*', '*', '*', '*', '*', '*', '*', '*', '*']
showBorder = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
isComputer = None

def show():
    global showBorder
    print(f'{showBorder[0]} | {showBorder[1]} | {showBorder[2]}')
    print(f'{showBorder[3]} | {showBorder[4]} | {showBorder[5]}')
    print(f'{showBorder[6]} | {showBorder[7]} | {showBorder[8]}')


def isCorrect(x):
    if x<0:
        return False
    elif x>8:
        return False
    else:
        return True
    
def isAvailable(index):
    global board
    return board[index]=='*'


def isFull():
    global board
    for i in range(len(board)):
        if board[i] == '*':
            return False
    return True

def checkThreePostion(in1,in2,in3,letter):
    global board
    return letter==board[in1]==board[in2]==board[in3]

def isWin(letter):
    rows = checkThreePostion(0,1,2,letter) or checkThreePostion(3,4,5,letter) or checkThreePostion(6,7,8,letter) 
    cols = checkThreePostion(0,3,6,letter) or checkThreePostion(1,4,7,letter) or checkThreePostion(2,5,8,letter)
    diogs= checkThreePostion(0,4,8,letter) or checkThreePostion(2,4,6,letter)
    return (rows or cols or diogs)

def makeMove(letter,index):
    global board,showBorder
    board[index]=letter
    showBorder[index]=letter



def main():
    global board,isComputer,showBorder,gameIsNotDone
    gameIsNotDone = True
    while(gameIsNotDone):
        board = ['*', '*', '*', '*', '*', '*', '*', '*', '*']
        showBorder = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
        isComputer = None
        play=input('1: Play\n2: exit\n')
        if play=='1':
            gameIsNotDone=True
            print('----------------')
            playType = int(input('1: Vs Computer\n2: Vs Another player\n'))
            print('----------------')
            isComputer = (playType == 1)
            firstPlayerLetter = str(input('o: O\nx: X\n'))
            secondPlayerLetter = ''
            if firstPlayerLetter == 'x':
                secondPlayerLetter = 'o'
            else:
                secondPlayerLetter = 'x'
            print('----------------')
            show()
            print('----------------')
            while(gameIsNotDone):

                while(gameIsNotDone):
                    pos=int(input('choose postion\t'))
                    print('----------------')
                    if isCorrect(pos) and isAvailable(pos):
                        makeMove(firstPlayerLetter,pos)
                        show()
                        print('----------------')
                        break
                if isWin(firstPlayerLetter):
                    print('You Win !!')
                    break
                elif isFull():
                    print('No Winners!!')
                    break

                while(gameIsNotDone):
                    if isComputer:
                        pos=randint(0,8)
                    else:
                        pos=int(input('choose postion\t'))
                        print('----------------')
                    if isCorrect(pos) and isAvailable(pos):
                        makeMove(secondPlayerLetter,pos)
                        show()
                        print('----------------')
                        break
                if isWin(secondPlayerLetter):
                    print('Second player win !!')
                    break
                elif isFull():
                    print('No Winners')
                    break
        else:
            gameIsNotDone=False
            # exit()

                



            
                    
                        


        


main()