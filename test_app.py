import os
import unittest
import json
import random
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie, helper_table


# TEST_DATABASE_URI = os.getenv('TEST_DATABASE_URI')
# CASTING_ASSISTANT = os.getenv('CASTING_ASSISTANT')
# CASTING_DIRECTOR = os.getenv('CASTING_DIRECTOR')
# EXECUTIVE_PRODUCER = os.getenv('EXECUTIVE_PRODUCER')

TEST_DATABASE_URI = 'postgresql://postgres:puru2000@localhost/casting_agency'
CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImlmLWJSbHpXMGdDeUM1eGE5Y3hSeSJ9.eyJpc3MiOiJodHRwczovL2R4cHIuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOTgzYzVkNjczZGVlMGJlODdjNWEyNSIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTU4NzAzNTQ1OCwiZXhwIjoxNTg3MDQyNjU4LCJhenAiOiI5Q3gzNmdWdHBydzhVRGpVa2NITERhMTFRNGpJcXplbyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.B2YSeeiD0j-vLmdTVQBX3p1R4--ainb-d9NGpWvWHYrNGgJDUnXELhYBCYJnn32HnxMXwwDxut7FBG_hh_Kww37b2cyjCFai2vOP_tfMLjLJ3bIGErO90ez_3zkCa6DCC3nt3ZpQI3z_1OhSlvmtr0al3VIs_vFiY01plmbUEtuYe9BxG_0v0MvHBt_Z1WrvIV5rtsmfWEe3ln5vewpQxzdzyQV7ZFIjnqLJvyvGbCVUH8q8dhZZ-may0rH3wlHxUttdva8k37g2j3IV9fjQwRUHCmooPHr15GwD2vT_YXDTFfFwb0AT1zamlKf9zw9szMmvnGdVeDbdiyTdyz2YPQ'
CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImlmLWJSbHpXMGdDeUM1eGE5Y3hSeSJ9.eyJpc3MiOiJodHRwczovL2R4cHIuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOTgzZTEwNjczZGVlMGJlODdjNWViMSIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTU4NzAzNTc1MywiZXhwIjoxNTg3MDQyOTUzLCJhenAiOiI5Q3gzNmdWdHBydzhVRGpVa2NITERhMTFRNGpJcXplbyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJlZGl0OmFjdG9ycyIsImVkaXQ6bW92aWVzIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.dlo6LJ05rn5XFs0RCYDHERIh12sSWSw3GZJoFNyG2bsSdKlzNnxcoiys76kvyS16XYwON-MnrHv9YbG1tDGg194Fy_C3g4EEWv9jwML5lLUsGyQsOX8R5MGY_yhwQI1jgEVSc2k2VKkQxOBaY1My5wtUopSm_Vn6UKDhuh-kD9HrGnNJ7li8YrK4-jm320yT4bnfgq0TSAleDLEbqIBLv954qHgaAiIjA1F4X9TQlXIahmj-Q1dG7XcpwirQ39RddNrYo9y7pDSSqSVWM5HausP5yq0AMAQe83iZsuLxJckE76NXoLWZZeTuFfp7_0shTAHVuqmSLR5VV7QOvqwzPg'
EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImlmLWJSbHpXMGdDeUM1eGE5Y3hSeSJ9.eyJpc3MiOiJodHRwczovL2R4cHIuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOTgzZWU5MzYwNzY0MGJkYzM4N2IyMyIsImF1ZCI6ImFnZW5jeSIsImlhdCI6MTU4NzAzNTk3MywiZXhwIjoxNTg3MDQzMTczLCJhenAiOiI5Q3gzNmdWdHBydzhVRGpVa2NITERhMTFRNGpJcXplbyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImFkZDptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImVkaXQ6YWN0b3JzIiwiZWRpdDptb3ZpZXMiLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.cyHyc0cPXo40ae2nephL-RTdY2B1j1vojrvWQBMQjLWnggQHhFJo4xolYpFIMoAPzw2SWWRwfo9ECvlhwohKWGHqOJ2bTQ0_x1d1LIGa6j5E47b5-AY0viBc9om1H8-PLiI0asjbBaGkk7QW2UGHRYpDvbtHKhKicPyVfdJ-js7sjyKO-midsVy0yj-Ph_Txn8P1Lx_iGkKtujPp_85Lf3Y07zuqjmVI7d1PtnnczyaQgaMCPGL305tp5A-zy9tKsXzZhkRandvXYWVwyNcJwjnGCT5UQDaZ7CyeuOG-uv-n2ChIAjDz_wAIkrcxPzv3UjBRjT-4rcOBcby6S34hXA'

class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.casting_assistant = CASTING_ASSISTANT
        self.casting_director = CASTING_DIRECTOR
        self.executive_producer = EXECUTIVE_PRODUCER
        setup_db(self.app)
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    '''
    RBAC TEST
    '''

    def test_post_actors_by_executive_producer_with_auth_200(self):
        response = self.client().post('/actors',
                                      headers={
                                          "Authorization": "Bearer {}"
                                          .format(self.executive_producer)
                                      },
                                      json={
                                          "name": "Alex",
                                          "gender": "male",
                                          "age": 25,
                                      })
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def test_post_actors_by_casting_assistant_without_auth_401(self):
        response = self.client().post('/actors',
                                      headers={
                                          "Authorization": "Bearer {}"
                                          .format(self.casting_assistant)
                                      },
                                      json={
                                          "name": "Brandon",
                                          "gender": "male",
                                          "age": 16
                                      })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'access_forbidden')

    def test_post_movies_by_executive_producer_with_auth_200(self):
        response = self.client().post('/movies',
                                      headers={
                                          "Authorization": "Bearer {}"
                                          .format(self.executive_producer)
                                      },
                                      json={
                                          "title": "Prestige",
                                          "release_date": "01/01/2005",
                                          'actors': [1]
                                      })

        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def test_post_movies_by_casting_assistant_without_auth_401(self):
        response = self.client().post('/movies',
                                      headers={
                                          "Authorization": "Bearer {}"
                                          .format(self.casting_assistant)
                                      },
                                      json={
                                          "title": "American Made",
                                          "release_date": "05/12/2018",
                                      })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'access_forbidden')

    def test_get_actors_by_casting_assistant_with_auth_200(self):
        response = self.client().get('/actors',
                                     headers={
                                         "Authorization": "Bearer {}"
                                         .format(self.casting_assistant)
                                     })
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def test_get_actors_by_casting_assistant_without_auth_401(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'no_auth_header')

    def test_get_movies_by_casting_assistant_with_auth_200(self):
        response = self.client().get('/movies',
                                     headers={
                                         "Authorization": "Bearer {}"
                                         .format(self.casting_assistant)
                                     })
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def test_get_movies_by_casting_assistant_without_auth_401(self):
        response = self.client().get('/movies')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'no_auth_header')

    def test_patch_actors_by_casting_director_with_auth_200(self):
        random_id = random.choice([actor.id for actor in Actor.query.all()])
        response = self.client().patch('/actors/{}'.format(random_id),
                                       headers={
            "Authorization": "Bearer {}".format(self.casting_director)
        },
            json={
            "name": "David",
            "gender": "other",
            "age": 10
        })

        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def test_patch_actors_by_casting_assistant_without_auth_401(self):
        random_id = random.choice([actor.id for actor in Actor.query.all()])
        response = self.client().patch('/actors/{}'.format(random_id),
                                       headers={
            "Authorization": "Bearer {}".format(self.casting_assistant)
        },
            json={
            "name": "David",
            "gender": "other",
            "age": 10
        })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'access_forbidden')

    def test_patch_movies_by_casting_director_with_auth_200(self):
        random_id = random.choice([movie.id for movie in Movie.query.all()])
        response = self.client().patch('/movies/{}'.format(random_id),
                                       headers={
            "Authorization": "Bearer {}".format(self.casting_director)
        },
            json={
            "title": "Joker",
            "release_date": "2019-10-1"
        })

        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    def test_patch_movies_by_casting_assistant_without_auth_401(self):
        random_id = random.choice([movie.id for movie in Movie.query.all()])
        response = self.client().patch('/movies/{}'.format(random_id),
                                       headers={
            "Authorization": "Bearer {}".format(self.casting_assistant)
        },
            json={
            "title": "Joker",
            "release_date": "2019-10-1"
        })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'access_forbidden')

    def test_delete_actors_by_casting_assistant_without_auth_401(self):
        random_id = random.choice([actor.id for actor in Actor.query.all()])
        response = self.client().delete('actors/{}'.format(random_id),
                                        headers={
                                            "Authorization": "Bearer {}"
                                            .format(self.casting_assistant)
        }
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'access_forbidden')

    def test_delete_actors_by_executive_producer_with_auth_200(self):
        random_id = random.choice([actor.id for actor in Actor.query.all()])
        response = self.client().delete('actors/{}'.format(random_id),
                                        headers={
                                            "Authorization": "Bearer {}"
                                            .format(self.executive_producer)
        }
        )
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

        def test_delete_movies_by_casting_assistant_without_auth_401(self):
            random_id = random.choice([movie.id for movie in Movie.query.all()])
            response = self.client().delete('movies/{}'.format(random_id),
                                            headers={
                                                "Authorization": "Bearer {}"
                                                .format(self.casting_assistant)
                                            }
            )
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['code'], 'access_forbidden')

    def test_delete_movies_by_executive_producer_with_auth_200(self):
        random_id = random.choice([movie.id for movie in Movie.query.all()])
        response = self.client().delete('movies/{}'.format(random_id),
                                        headers={
                                            "Authorization": "Bearer {}"
                                            .format(self.executive_producer)
                                        }
        )
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

if __name__ == '__main__':
    unittest.TestLoader.sortTestMethodsUsing = None
    unittest.main()