import os
import requests

from flask import render_template, request, redirect, url_for, flash, abort
from app import app, db
from models import Match, User
from datetime import datetime
from sqlalchemy import func
from geoalchemy2.functions import ST_DWithin
from geoalchemy2.elements import WKTElement

GOOGLE_MAPS_API_KEY = app.config.get("GOOGLE_MAPS_API_KEY")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/available_matches")
def available_matches():
    matches = Match.query.filter_by(is_full=False).order_by(Match.date_time).all()
    return render_template("available_matches.html", matches=matches)


@app.route("/full_matches")
def full_matches():
    matches = Match.query.filter_by(is_full=True).order_by(Match.date_time).all()
    return render_template("full_matches.html", matches=matches)


def geocode_address(address):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    return None, None


@app.route("/create_match", methods=["GET", "POST"])
def create_match():
    if request.method == 'POST':
        new_match = Match(
            players_present=int(request.form['players_present']),
            level_present=request.form['level_present'],
            level_required=request.form['level_required'],
            pitch_address=request.form['pitch_address'],
            date_time=datetime.strptime(request.form['date_time'], '%Y-%m-%dT%H:%M'),
            rental_price=float(request.form['rental_price']),
            description=request.form['description']
        )
        db.session.add(new_match)
        db.session.commit()
        flash('New match created successfully!', 'success')
        return redirect(url_for('available_matches'))
    return render_template('create_match.html')


@app.route("/join_match/<int:match_id>", methods=["POST"])
def join_match(match_id):
    match = Match.query.get_or_404(match_id)
    if match.is_full:
        flash("This match is already full!", "error")
    else:
        try:
            new_player = User(
                name=request.form["player_name"],
                level=request.form["player_level"],
                match_id=match.id,
            )
            db.session.add(new_player)
            match.players_present += 1
            if match.players_present == 4:
                match.is_full = True
            db.session.commit()
            flash("You have successfully joined the match!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error joining match: {str(e)}", "error")
    return redirect(url_for("available_matches"))


@app.route("/search_matches", methods=["GET", "POST"])
def search_matches():
    if request.method == "POST":
        try:
            user_lat = float(request.form["latitude"])
            user_lon = float(request.form["longitude"])
            radius = float(request.form["radius"])  # in kilometers

            user_location = WKTElement(f"POINT({user_lon} {user_lat})", srid=4326)

            nearby_matches = (
                Match.query.filter(
                    ST_DWithin(
                        Match.location, user_location, radius * 1000
                    )  # Convert km to meters
                )
                .filter_by(is_full=False)
                .order_by(Match.date_time)
                .all()
            )

            return render_template("search_results.html", matches=nearby_matches)
        except Exception as e:
            flash(f"Error searching matches: {str(e)}", "error")

    return render_template("search_form.html")


@app.route("/match/<int:match_id>")
def match_details(match_id):
    match = Match.query.get_or_404(match_id)
    return render_template("match_details.html", match=match)


@app.route("/edit_match/<int:match_id>", methods=["GET", "POST"])
def edit_match(match_id):
    match = Match.query.get_or_404(match_id)
    if request.method == "POST":
        try:
            match.level_required = request.form["level_required"]
            match.pitch_address = request.form["pitch_address"]
            match.date_time = datetime.strptime(
                request.form["date_time"], "%Y-%m-%dT%H:%M"
            )
            match.rental_price = float(request.form["rental_price"])
            db.session.commit()
            flash("Match updated successfully!", "success")
            return redirect(url_for("match_details", match_id=match.id))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating match: {str(e)}", "error")
    return render_template("edit_match.html", match=match)


@app.route("/cancel_match/<int:match_id>", methods=["POST"])
def cancel_match(match_id):
    match = Match.query.get_or_404(match_id)
    try:
        db.session.delete(match)
        db.session.commit()
        flash("Match cancelled successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error cancelling match: {str(e)}", "error")
    return redirect(url_for("available_matches"))


@app.route("/leave_match/<int:match_id>/<int:player_id>", methods=["POST"])
def leave_match(match_id, player_id):
    match = Match.query.get_or_404(match_id)
    player = User.query.get_or_404(player_id)
    if player.match_id != match.id:
        abort(400)
    try:
        db.session.delete(player)
        match.players_present -= 1
        match.is_full = False
        db.session.commit()
        flash("You have left the match successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error leaving match: {str(e)}", "error")
    return redirect(url_for("available_matches"))
