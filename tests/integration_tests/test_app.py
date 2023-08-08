from tests.conftest import TEST_CLUBS_FILE, TEST_COMPETITIONS_FILE, TEST_BOOKINGS_FILE
from app import models


class TestClass:
    def mocking_json_files(self, mocker):
        mocker.patch.object(models.Club, '_json_file_path', TEST_CLUBS_FILE)
        mocker.patch.object(models.Competition, '_json_file_path', TEST_COMPETITIONS_FILE)
        mocker.patch.object(models.Booking, '_json_file_path', TEST_BOOKINGS_FILE)

    def test_index_should_status_code_ok(self, client, mocker):
        self.mocking_json_files(mocker)
        response = client.get('/')
        assert response.status_code == 200

    def test_index_rendering(self, client, mocker):
        self.mocking_json_files(mocker)
        response = client.get('/')
        # Decode pour avoir le html de la page
        data = response.data.decode()
        # data.find() renvoie -1 quand non trouvé
        assert data.find("Welcome to the GUDLFT Registration Portal!") != -1

    def test_get_summary_should_405(self, client, mocker):
        """
        Only supports POST requests. Get should http 405.
        """
        self.mocking_json_files(mocker)
        response = client.get('/showSummary')
        assert response.status_code == 405

    def test_login_user(self, client, mocker):
        # Mocking club json file to use test version
        self.mocking_json_files(mocker)

        response = client.post('/showSummary',data=dict(email='john@simplylift.co'),follow_redirects=True)
        data = response.data.decode()
        assert response.status_code == 200
        # Should not be redirected to index
        assert data.find("Welcome to the GUDLFT Registration Portal!") == -1
        # Should welcome user
        assert data.find("Welcome, john@simplylift.co") != -1

    def test_index_should_render_table(self, client, mocker):
        self.mocking_json_files(mocker)
        response = client.get('/')
        data = response.data.decode()
        assert data.find("<th>Club</th>") != -1
        assert data.find("<td>Iron Temple</td>") != -1

