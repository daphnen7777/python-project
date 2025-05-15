import pygame
import sys
import random
from time import sleep
# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# 게임 화면의 가로와 세로 크기
padWidth = 480
padHeight = 640
# 운석 및 생명 아이콘 이미지 파일 경로
rockImage = ['11.png', '12.png', '13.png', '14.png', '15.png', '16.png', '17.png',
             '18.png', '19.png', '20.png', '21.png', '22.png', '23.png']
heartImage = 'heart.png'  # 생명 아이콘 이미지 파일
def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))
    
def drawLives(lives):
    # 생명 아이콘을 화면에 반복하여 그립니다.
    for i in range(lives):
        drawObject(heart, 10 + i * 40, 10)  # 10 + i * 40: 위치를 옆으로 이동시키며 생명 아이콘을 표시
        
def writeScore(count): #유저가 파괴한 운석 개수 카운트 및 출력
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 15)
    text = font.render('파괴한 운석 수:' +str(count), True, (255,255,255))
    gamePad.blit(text,(360, 0))

def writeUlt(count): #유저가 파괴한 운석 개수 카운트 및 출력
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 15)
    text = font.render('ult:' +str(count), True, (255,255,255))
    gamePad.blit(text,(300, 0))

def drawGameOver():  #게임 오버시 화면 및 사운드 출력해주는 함수
    font = pygame.font.SysFont(None, 72)
    text = font.render('GAME OVER', True, WHITE)
    text_rect = text.get_rect(center=(padWidth // 2, padHeight // 2.5))
    gamePad.blit(text, text_rect)
    font = pygame.font.SysFont(None, 32)
    text = font.render('Press r to Retry', True, WHITE)
    text_rect = text.get_rect(center=(padWidth // 2, padHeight // 2.0))  #게임 오버시 유저에게 재시작 할건지 묻는 텍스트
    gamePad.blit(text, text_rect)
    text = font.render('Press q to Quit', True, WHITE)
    text_rect = text.get_rect(center=(padWidth // 2, padHeight // 1.8))  #게임 오버시 유저에게 게임을 종료 할건지 묻는 텍스트
    gamePad.blit(text, text_rect)
    pygame.display.update()
    pygame.mixer.music.stop()  # 게임 오버 시 배경음악 멈춤
    gameOverSound.play()  # 게임 오버 사운드 재생
    sleep(2)  # 잠시 대기하여 게임 오버 메시지를 볼 수 있게 함
    
def initGame():     #게임에 필요한 파일들 선언하는 함수
    global gamePad, clock, background, fighter, missile, explosion, strongMissile, heart
    global gameOverSound, damageSound, explodeSound
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('PyShooting')
    background = pygame.image.load('background.png')
    fighter = pygame.image.load('fighter.png')
    missile = pygame.image.load('missile.png')
    explosion = pygame.image.load('explosion.png')
    strongMissile = pygame.image.load('strong_missile.png')  # 강력한 미사일 이미지
    heart = pygame.image.load(heartImage)  # 생명 아이콘 이미지
    # 사운드 초기화
    pygame.mixer.init()
    explodeSound = pygame.mixer.Sound('explosion.mp3')
    gameOverSound = pygame.mixer.Sound('game_over_sound.mp3')
    damageSound = pygame.mixer.Sound('damage_sound.mp3')
    clock = pygame.time.Clock()

def runGame():  #게임 실행 함수
    global gamePad, clock, background, fighter, missile, explosion, strongMissile, heart
    global gameOverSound, damageSound, explodeSound
    # 전투기 크기
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]
    # 전투기 초기 위치 (x, y)
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0
    fighterY = 0
    missileXY = []
    missileHoldStart = 0  # 스페이스 바를 누르기 시작한 시간을 기록하는 변수
    #미사일 크기
    missile_size = missile.get_rect().size
    missileWidth = missile_size[0]
    missileHeight = missile_size[1]
    strongMissile_size = strongMissile.get_rect().size
    strongMissileWidth = strongMissile_size[0]
    strongMissileHeight = strongMissile_size[1]
    # 운석 초기화
    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 2
    isShot = False
    shotCount = 0
    shotCountforult = 0
    lives = 3  # 초기 목숨 수
    ultimate = 0
    onGame = True
    gameOver = False
    pygame.mixer.music.load('background_music.mp3')
    pygame.mixer.music.play(-1)            # 무한 반복 재생
    while onGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 게임 프로그램 종료
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # 전투기 왼쪽으로 이동
                    fighterX = -5
                elif event.key == pygame.K_RIGHT:  # 전투기 오른쪽으로 이동
                    fighterX = 5
                elif event.key == pygame.K_UP:
                    fighterY = -5
                elif event.key == pygame.K_DOWN:
                    fighterY = 5
                elif event.key == pygame.K_SPACE:
                    if missileHoldStart == 0:  # 스페이스 바를 처음 누른 경우
                        missileHoldStart = pygame.time.get_ticks()  # 시작 시간 기록
                elif event.key == pygame.K_r and gameOver:  # 게임 오버 상태에서 R 키를 눌러서 재시작
                    runGame()
            if event.type == pygame.KEYUP:  # 방향키를 떼면 전투기 멈춤
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    fighterY = 0
                elif event.key == pygame.K_SPACE:
                    missileHoldDuration = pygame.time.get_ticks() - missileHoldStart  # 스페이스 바를 누른 시간 계산
                    missileX = x + fighterWidth / 2 - missileWidth / 2
                    missileY = y - missileHeight
                    missileSpeed = 10 + min(missileHoldDuration / 100, 10)  # 속도 조절
                    # missileImage = strongMissile if missileHoldDuration > 500 else missile  # 강력한 미사일 이미지 선택
                    missileImage = missile
                    missileXY.append([missileX, missileY, missileSpeed, missileImage])  # 미사일 정보 저장
                    missileHoldStart = 0  # 스페이스 바를 떼면 시간 리셋
                    
                elif event.key == pygame.K_x:  # X 키를 눌러 필살기 출력
                    if ultimate >= 1:
                        ultimate -= 1
                        missileImage = strongMissile
                        missileX = x + fighterWidth / 2 - strongMissileWidth / 2
                        missileY = y - strongMissileHeight
                        missileSpeed = 10 + min(missileHoldDuration / 100, 10)  # 속도 조절
                        missileXY.append([missileX, missileY, missileSpeed, missileImage])  # 미사일 정보 저장
                        missileHoldStart = 0  # 스페이스 바를 떼면 시간 리셋
        if not gameOver:
            # 전투기 위치 재조정
            x += fighterX
            y += fighterY
            if x < 0:
                x = 0
            elif x > padWidth - fighterWidth:
                x = padWidth - fighterWidth
            if y < 0:
                y = 0
            elif y > padHeight - fighterHeight:
                y = padHeight - fighterHeight
            gamePad.fill(BLACK)
            drawObject(background, 0, 0)
            drawObject(fighter, x, y)
            drawLives(lives)  # 생명 아이콘으로 표시
            # 미사일 처리
           
            if len(missileXY) != 0:
                for i, (bx, by, speed, img) in enumerate(missileXY):
                    by -= speed
                    missileXY[i][1] = by
                    if by < rockY:
                        if (bx + missileWidth / 2  > rockX) and (bx + missileWidth / 2 < rockX + rockWidth):
                            missileXY.remove([bx, by, speed, img])
                            isShot = True
                            shotCount += 1
                            shotCountforult += 1
                    if by <= 0:
                        try:
                            missileXY.remove([bx, by, speed, img])
                        except:
                            pass
            if len(missileXY) != 0:
                for bx, by, _, img in missileXY:
                    drawObject(img, bx, by)

            if shotCountforult == 3:
                ultimate += 1
                shotCountforult -= 3
            
            
            # 암석 처리
            writeScore(shotCount)
            writeUlt(ultimate)
                        
            rockY += rockSpeed
            if rockY > padHeight:
                rock = pygame.image.load(random.choice(rockImage))
                rockSize = rock.get_rect().size
                rockWidth = rockSize[0]
                rockHeight = rockSize[1]
                rockX = random.randrange(0, padWidth - rockWidth)
                rockY = 0
                # 바닥에 떨어진 암석이 있을 때 목숨 차감
                lives -= 1
                damageSound.play()  # 데미지 사운드 재생
                if lives <= 0:
                    gameOver = True
                    drawGameOver()
                else:
                    sleep(1)  # 잠시 대기하여 충돌을 인식할 시간을 줌
            drawObject(rock, rockX, rockY)
            # 전투기와 암석 충돌 체크
            if y < rockY + rockHeight and x + fighterWidth > rockX and x < rockX + rockWidth:
                lives -= 3  # 목숨 차감
                damageSound.play()  # 데미지 사운드 재생
                if lives <= 0:
                    gameOver = True
                    drawGameOver()
                else:
                    rock = pygame.image.load(random.choice(rockImage))
                    rockSize = rock.get_rect().size
                    rockWidth = rockSize[0]
                    rockHeight = rockSize[1]
                    rockX = random.randrange(0, padWidth - rockWidth)
                    rockY = 0
                    sleep(1)  # 잠시 대기하여 충돌을 인식할 시간을 줌

            if isShot:
                drawObject(explosion, rockX, rockY)
                explodeSound.play()
                rock = pygame.image.load(random.choice(rockImage))
                rockSize = rock.get_rect().size
                rockWidth = rockSize[0]
                rockHeight = rockSize[1]
                rockX = random.randrange(0, padWidth - rockWidth)
                rockY = 0
                isShot = False

            pygame.display.update()
            clock.tick(60)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 게임 프로그램 종료
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # Q 키를 눌러서 종료
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_r:  # R 키를 눌러서 재시작
                        runGame()
    
    pygame.quit()

initGame()
runGame()