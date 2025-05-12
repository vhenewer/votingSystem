from dao.BaseDao import Dao
import sys

sys.path.append("/Users/argenkulzhanov/Desktop/Designer/project/classes")
from classes.candidate import Candidate

class CandidateDAO(Dao):
    def __init__(self, db_path):
        super().__init__(db_path)

    def insert(self, candidate: Candidate):
        query = "INSERT INTO Candidates (election_name, name, party, profile) VALUES (? ,? ,? ,? )"
        self.execute_query(query, (candidate.get_election_name(), candidate.get_name(), candidate.get_party(), candidate.get_profile()))
        self._connection.commit()
        return self._cursor.lastrowid


    def get_candidates_by_election(self, election_name):
        query = "SELECT candidate_id, election_name, name, party, profile FROM Candidates WHERE election_name = ?"
        result = self.fetch_all(query, (election_name,))

        candidates = []
        for row in result:
            candidate = Candidate(row[1], row[2], row[3], row[4])
            candidate.set_id(row[0])
            candidates.append(candidate)

        return candidates

    def find_by_id_use_election(self, candidate_id, election_name):
        query = "SELECT * FROM Candidates WHERE candidate_id = ? AND election_name = ?"
        row = self.fetch_one(query, (candidate_id, election_name))

        # Если результат найден
        if row:
            # Предполагаем, что у нас есть колонка с id (например, row[0] - это id)
            # и остальные столбцы идут по порядку: election_name, name, party, profile
            return Candidate(row[1], row[2], row[3], row[4])  # Возвращаем кандидата

        # Если кандидат не найден
        return None

