from threading import Lock
from flask import Flask, render_template, session, request, redirect, url_for, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

from .. import socketio
from . import home
from ..models import dataManipulator
thread = None
thread_lock = Lock()

dataHelper = dataManipulator()