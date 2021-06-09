

def init(app_, sm_):
    global app
    app = app_
    global sm
    sm = sm_

def db_init(db_):
    global db
    db = db_


def calculate_direction(
        up: bool,
        down: bool,
        left: bool,
        right: bool,
        speed: int,
        turn_diff: int
    ):
    # Takes motor states and calculates speeds and directions of each motor.

    # First, find which base direction we're going:
    main_dir = "stop"
    if up:
        main_dir = "forward"

    elif down:
        main_dir = "backward"

    if up and down:
        # Both directions are pressed
        #   => Go nowhere
        return [
            {
                "id": 1,
                "state": "stop"
            },
            {
                "id": 2,
                "state": "stop"
            }
        ]

    # Define our speeds

    # 1 = left
    # 2 = right
    if up or down:
        # If we're moving, do it faster
        motors = {
            1: int(speed), # Copy
            2: int(speed) 
        }

    else:
        # Do a tight turn - forward & reverse
        if left and not right:
            m1 = "backward"
            m2 = "forward"

        elif right and not left:
            m1 = "forward"
            m2 = "backward"

        else:
            # Do nothing
            return [
                {
                    "id": 1,
                    "state": "stop"
                },
                {
                    "id": 2,
                    "state": "stop"
                }
            ]


        return [
            {
                "id": 1,
                "state": m1,
                "speed": speed
            },
            {
                "id": 2,
                "state": m2,
                "speed": speed
            }
        ]
        

    # Find out if we're turning
    if left or right:
        if left:
            speedup = 2
            slowdown = 1

        elif right:
            speedup = 1
            slowdown = 2

        if left and right:
            # Just go forward
            return [
                {
                    "id": 1,
                    "state": main_dir,
                    "speed": speed
                },
                {
                    "id": 2,
                    "state": main_dir,
                    "speed": speed
                }
            ]

        # We want to speed up right
        motors[speedup] += turn_diff
        if motors[speedup] > 100:
            motors[slowdown] -= motors[speedup] - 100 # Bump the other down so we don't exceed 100
            motors[speedup] = 100 # And cap off main

    # Send it off
    return [
        {
            "id": 1,
            "state": main_dir,
            "speed": motors[1]
        },
        {
            "id": 2,
            "state": main_dir,
            "speed": motors[2]
        }
    ]


def change_direction():
    # Find each button
    ids = sm.ids["drive_screen"].ids

    states = [
        ids["up"],
        ids["down"],
        ids["left"],
        ids["right"]
    ]

    bool_states = []

    for button in states:
        bool_states.append(button.state == "down") 

    return calculate_direction(
        *bool_states,
        db["speed"],
        db["turn_speed"]
    )


