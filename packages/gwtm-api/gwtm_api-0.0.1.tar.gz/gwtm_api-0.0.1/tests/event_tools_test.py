import sys

sys.path.insert(0, '../src')

import gwtm_api

if __name__ == "__main__":
    token = "X8yASL3YVhZhgeOYSf0cIinjjLvE0Wl00Eb-Rw"
    gwtm_api.event_tools.plot_coverage(
        graceid="S240422ed",
        api_token=token
    )
    # pointings = gwtm_api.Pointing.get(
    #     graceid = "S240422ed",
    #     instrument="DECam",
    #     status="completed",
    #     api_token=token
    # )

    # print(len(pointings))

    # prob, area = gwtm_api.event_tools.calculate_coverage(
    #     api_token=token,
    #     graceid="S240422ed",
    #     pointings=pointings,
    #     cache=False,
    #     approximate=False
    # )
    # print(prob, area)