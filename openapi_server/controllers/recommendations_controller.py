import connexion
from typing import Dict, Tuple, Union, List

from openapi_server.models.like import Like
from openapi_server.models.play import Play
from openapi_server.models.track import Track
# NUEVOS IMPORTS
from openapi_server.models.comment import Comment
from openapi_server.models.rating import Rating
from openapi_server import util

# BD Temporal
_PLAYS_DB = []
_LIKES_DB = []
_COMMENTS_DB = [] # Nuevo
_RATINGS_DB = []  # Nuevo

# --- PLAYS & LIKES (Igual que antes) ---
def add_play(body):
    if connexion.request.is_json:
        _PLAYS_DB.append(body)
    return "Play registered", 201

def add_like(body):
    if connexion.request.is_json:
        _LIKES_DB.append(body)
    return "Like registered", 201

def get_user_plays(id_user): return [p for p in _PLAYS_DB if p.user_id == id_user]
def get_user_likes(id_user): return [l for l in _LIKES_DB if l.user_id == id_user]
def get_track_plays(id_track): return [p for p in _PLAYS_DB if p.track_id == id_track]
def get_track_likes(id_track): return [l for l in _LIKES_DB if l.track_id == id_track]

# --- NUEVO: COMENTARIOS & VALORACIONES ---

def add_comment(body):
    """Añadir comentario con moderación"""
    if connexion.request.is_json:
        comment_obj = Comment.from_dict(body)
        comment_obj.status = 'pending' # Moderación inicial
        _COMMENTS_DB.append(comment_obj)
        print(f"--> Comentario pendiente: {comment_obj.content}")
    return "Comment added (pending)", 201

def get_track_comments(id_track):
    """Solo devuelve comentarios aprobados"""
    return [c for c in _COMMENTS_DB if c.track_id == id_track and c.status == 'approved']

def moderate_comment(id_comment, action):
    """Simulación Admin"""
    for c in _COMMENTS_DB:
        if c.id == id_comment:
            if action == 'approve': c.status = 'approved'
            elif action == 'reject': c.status = 'rejected'
            return f"Comment {action}d", 200
    return "Not found", 404

def delete_comment(id_comment):
    global _COMMENTS_DB
    initial = len(_COMMENTS_DB)
    _COMMENTS_DB = [c for c in _COMMENTS_DB if c.id != id_comment]
    if len(_COMMENTS_DB) < initial: return "Deleted", 200
    return "Not found", 404

def add_rating(body):
    if connexion.request.is_json:
        r = Rating.from_dict(body)
        if 1 <= r.score <= 5:
            _RATINGS_DB.append(r)
            return "Rating added", 201
    return "Invalid score", 400

def get_track_ratings(id_track):
    return [r for r in _RATINGS_DB if r.track_id == id_track]

# Stubs restantes
def get_artist_plays(id_artist): return []
def get_artist_top_tracks(id_artist): return []
def get_recommended_tracks(id_user, type=None): return []
def get_top_tracks(): return []