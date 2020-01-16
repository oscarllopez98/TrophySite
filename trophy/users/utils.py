import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from trophy import mail

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	#Path to the selected image
	picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

	#Resize images for website efficiency
	output_size = (125,125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	#Save image
	i.save(picture_path)
	return picture_fn

#Sends reset password email to the user's email
def send_reset_email(user):
	#Default param is 1800 (seconds)
	token = user.get_reset_token()
	msg = Message('Password Reset Request',
		sender='noreply@demo.com',
		recipients=[user.email])
	#_external gives a absolute link, not a relative one
	msg.body = f''' To reset your password, visit the following link
{url_for('users.reset_token',token=token,_external=True)}

If you did make this request then simply ignore this email and no changes will be made.
	'''
	#Send email
	mail.send(msg)
