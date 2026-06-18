"""
this class define the errors that can be define

"""


class RankInvalid(Exception):
    pass


class AgentNotExists(Exception):
    pass


class InvalidDifficulty(Exception):
    pass


class InvalidImportance(Exception):
    pass


class MissionNotExists(Exception):
    pass


class MissionNotNew(Exception):
    pass


class InactiveAgent(Exception):
    pass


class AgentOverTheMissionsLimit(Exception):
    pass

class CriticalForSenior(Exception):
    pass

class CriticalForJunior(Exception):
    pass

class StartUnassignedMissionError(Exception):
    pass

class CompleteMissionNotInProgress(Exception):
    pass

class CancelCompleteMission(Exception):
    pass