from unittest import TestCase
from app import app
from models import db, default_cupcake, Cupcake

class CupcakeTestClass(TestCase):
    
    def setUp(self):
        with app.app_context():
            Cupcake.query.delete()
            db.session.commit()
            
            cupcake = Cupcake(flavor="example", size="large", rating=5, image="image.jpg")
            db.session.add(cupcake)
            db.session.commit()
            
            self.cupcake_id = cupcake.id
            
    def tearDown(self):
        with app.app_context():
            db.session.rollback()
            
    def test_show_cupcakes(self):
        with app.test_client() as client:
            resp = client.get('/api/cupcakes')
            self.assertEqual(resp.status_code, 200)
            
            self.assertEqual(
                resp.json,
                [{
                    "id": self.cupcake_id,
                    "flavor": "example",
                    "size": "large",
                    "rating": 5,
                    "image": "image.jpg",
                }])
            
    def test_add_cupcake(self):
        with app.test_client() as client:
            resp = client.post(
                '/api/cupcakes', json={
                "flavor": "example2",
                "size": "medium",
                "rating": 8,
                "image": "picture.jpg"
                })
            self.assertEqual(resp.status_code, 200)
            
            data = resp.json['cupcake']
            
            self.assertEqual(data['flavor'], 'example2')
            self.assertEqual(data['size'], 'medium')
            self.assertEqual(data['rating'], 8)
            self.assertEqual(data['image'], 'picture.jpg')
            
    def test_show_cupcake(self):
        with app.test_client() as client:
            resp = client.get(f'/api/cupcakes/{self.cupcake_id}')
            self.assertEqual(resp.status_code, 200)
            
            self.assertEqual(
            resp.json, {
            "id": self.cupcake_id,
            "flavor": "example",
            "size": "large",
            "rating": 5,
            "image": "image.jpg"
            })
            
    def test_update_cupcake(self):
        with app.test_client() as client:
            resp = client.patch(
                f'/api/cupcakes/{self.cupcake_id}', json={
                "flavor": "new flavor",
                "size": "small"   
                })
            
            self.assertEqual(resp.status_code, 200)
            
            data = resp.json['cupcake']
            
            self.assertEqual(data['flavor'], 'new flavor')
            self.assertEqual(data['size'], 'small')
            
    def test_delete_cupcake(self):
        with app.test_client() as client:
            resp = client.delete(f'/api/cupcakes/{self.cupcake_id}')
            self.assertEqual(resp.status_code, 200)
            
            resp = client.delete(f'/api/cupcakes/{self.cupcake_id}')
            self.assertEqual(resp.status_code, 404) #should no longer exist