from pico2d import load_image, get_time


from state_machine import StateMachine, time_out, space_down, right_down, left_down, right_up, left_up, start_event


# 상태를 클래스를 통해서 정의함.
class Idle:
    @staticmethod #이 뒤에 이어 오는 함수를 staticmethod 함수로 간주하겠다 >> 멤버 함수가 아닌, 객체와 상관 없는 함수 >> 클래스의 이름으로 함수를 그룹화
    def enter(boy, e):
        # 현재 시간 저장
        if left_up(e) or right_down(e):
            boy.image_dir = -1
            boy.action = 2

        elif right_up(e) or left_down(e) or start_event(e):
            boy.image_dir = 1
            boy.action = 3
        boy.start_time = get_time()
        pass

    @staticmethod
    def exit(boy, e):

        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 3:
            boy.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass


class Sleep:
    @staticmethod
    def enter(boy, e):
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        pass

    @staticmethod
    def draw(boy):

        if boy.image_dir == 1:
            boy.image.clip_composite_draw(
                boy.frame*100, 300, 100, 100,
                3.141592 / 2, #90도 회전
                '', #좌우상하 반전
                boy.x - 25, boy.y - 25, 100, 100
            )
        elif boy.image_dir == -1:
            boy.image.clip_composite_draw(
                boy.frame*100, 300, 100, 100,
                3.141592 / 2, #90도 회전
                'v', #좌우상하 반전
                boy.x + 25, boy.y - 25, 100, 100
            )
        pass

class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e):

            boy.dir = 1 #오른쪽 방향
            boy.action = 1

        elif left_down(e) or right_up(e):
            boy.dir = -1
            boy.action = 0

        boy.frame = 0
        pass

    @staticmethod
    def exit(boy, e):

        pass

    @staticmethod
    def do(boy):
        boy.x += boy.dir * 5
        boy.frame = (boy.frame + 1)%8
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100,
                            boy.x, boy.y)
        pass

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.image_dir = 1
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self) # 소년 객체의 state machine 생성
        self.state_machine.start(Idle) # 초기 상태가 ???로 설정
        self.state_machine.set_transitions(
            {
                Run: {right_down : Idle, right_up : Idle, left_down : Idle, left_up : Idle}, # Run 상태에서 어떤 event가 들어와도 처리하지 않겠다
                Idle : { time_out : Sleep , right_down : Run, right_up : Idle, left_down : Run, left_up : Idle},
                Sleep: { space_down : Idle, right_down : Run, right_up : Idle, left_down : Run, left_up : Idle}

            }
        )
    def update(self):
        #self.frame = (self.frame + 1) % 8
        self.state_machine.update()

    def handle_event(self, event):
        # event : 입력 이벤트
        # 우리가 state machine 전달해줄 것은 tuple
        self.state_machine.add_event(('INPUT', event))


    def draw(self):
        self.state_machine.draw()
