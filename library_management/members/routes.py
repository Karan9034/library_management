from flask import Blueprint, redirect, render_template, flash, request, url_for
from library_management import db
from library_management.models import Member, Transaction, Book
from library_management.members.forms import RegisterForm, EditForm

members = Blueprint("members", __name__)

@members.route('/members')
def all_members():
    page = request.args.get('page', 1, type=int)
    members = Member.query.order_by(Member.member_id.asc()).paginate(page=page, per_page=20)
    return render_template("members.html", title="Members", members=members, data=members.items)

@members.route('/members/register', methods=['GET', 'POST'])
def register_member():
    register_form = RegisterForm()
    if request.method=='POST' and register_form.validate_on_submit():
        name = register_form.name.data
        email = register_form.email.data
        member = Member.query.filter_by(email=email).first()
        if member:
            flash('Member already exists', 'info')
            return redirect(url_for('members.all_members'))
        member = Member(name=name, email=email)
        db.session.add(member)
        db.session.commit()
        flash(f'Member Registered with ID {member.member_id}', 'success')
        return redirect(url_for('members.all_members'))
    return render_template('register_member.html', register_form=register_form, title='Register Member')

@members.route('/members/search', methods=['POST'])
def search():
    query = request.form.get('search')
    members_by_name = Member.query.filter(Member.name.contains(query)).all()
    members_by_email = Member.query.filter(Member.email.contains(query)).all()
    members = members_by_name + members_by_email
    members = set(members)
    members = list(members)
    members = sorted(members, key=lambda x: x.member_id, reverse=False)
    return render_template('members.html', title=f"Search {query}", data=members)

@members.route('/member/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    member = Member.query.get_or_404(id)
    edit_form = EditForm()
    if request.method == 'POST' and edit_form.validate_on_submit():
        member.name = edit_form.name.data
        member.email = edit_form.email.data
        db.session.commit()
        flash('The member details have been updated!', 'success')
        return redirect(url_for('members.all_members'))
    elif request.method == 'GET':
        edit_form.name.data = member.name
        edit_form.email.data = member.email
    return render_template('edit_member.html', title=f"Member {member.member_id}", edit_form=edit_form)
