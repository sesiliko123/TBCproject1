from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, PasswordField, SelectField, BooleanField, FloatField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Optional

class RegisterForm(FlaskForm):
    username = StringField("მომხმარებელი", validators=[DataRequired(), Length(min=4, max=25)])
    first_name = StringField("სახელი", validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField("გვარი", validators=[DataRequired(), Length(min=2, max=50)])
    gender = SelectField("სქესი", choices=[("მდედრობითი", "მდედრობითი"), ("მამრობითი", "მამრობითი")], validators=[DataRequired()])
    password = PasswordField("პაროლი", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("გაიმეორე პაროლი", validators=[DataRequired(), EqualTo("password", message="პაროლები არ ემთხვევა")])
    submit = SubmitField("რეგისტრაცია")


class LoginForm(FlaskForm):
    username = StringField("მომხმარებელი", validators=[DataRequired()])
    password = PasswordField("პაროლი", validators=[DataRequired()])
    submit = SubmitField("შესვლა")


class CategoryForm(FlaskForm):
    category = SelectField('კატეგორიები:', choices=[
        ('მობილური', '📱 მობილური'),
        ('ტაბი', '📲 ტაბი'),
        ('ლეპტოპი', '💻 ლეპტოპი'),
        ('ტელევიზორი', '📺 ტელევიზორი'),
        ('მონიტორი', '🖥️ მონიტორი'),
        ('კონსოლი', '🎮 კონსოლი'),
        ('ყურსასმენი', '🎧 ყურსასმენი'),
        ('სმარტ საათი', '⌚ სმარტ საათი')
    ], validators=[DataRequired()])
    submit = SubmitField('➡️ გაგრძელება')


class ProductForm(FlaskForm):
    name = StringField('დასახელება', validators=[DataRequired()])
    price = FloatField('ფასი', validators=[DataRequired()])
    image = FileField('სურათი', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

    screen_size = StringField('ეკრანის ზომა', validators=[Optional()])
    resolution = StringField('რეზოლუცია', validators=[Optional()])
    refresh_rate = StringField('განახლების სიხშირე', validators=[Optional()])
    screen_type = StringField('ეკრანის ტიპი', validators=[Optional()])
    storage = StringField('შიდა მეხსიერება', validators=[Optional()])
    bluetooth = StringField('Bluetooth', validators=[Optional()])
    ram = StringField('ოპერატიული მეხსიერება', validators=[Optional()])
    battery = StringField('ელემენტი', validators=[Optional()])
    charging_time = StringField('დამუხტვის დრო', validators=[Optional()])
    type_c = StringField('Type-C', validators=[Optional()])
    viewing_angle = StringField('ხედვის კუთხე', validators=[Optional()])
    work_time = StringField('სამუშაო დრო', validators=[Optional()])
    noise_cancellation = BooleanField('ხმის დახშობა')

    # კონსოლისთვის
    processor = StringField('პროცესორი', validators=[Optional()])
    cores = StringField('ბირთვები', validators=[Optional()])
    frequency = StringField('სიხშირე', validators=[Optional()])

    submit = SubmitField('შენახვა')



class ProfileImageForm(FlaskForm):
    profile_image = FileField('პროფილის ფოტო', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'დაშვებულია მხოლოდ სურათის ფაილები')
    ])
    submit = SubmitField('ატვირთვა')


class ReviewForm(FlaskForm):
    rating = SelectField(
        'შეფასება',
        choices=[(5, '★★★★★'), (4, '★★★★☆'), (3, '★★★☆☆'), (2, '★★☆☆☆'), (1, '★☆☆☆☆')],
        coerce=int,
        validators=[DataRequired()]
    )
    comment = TextAreaField('კომენტარი', validators=[DataRequired()])
    submit = SubmitField('გაგზავნა')
