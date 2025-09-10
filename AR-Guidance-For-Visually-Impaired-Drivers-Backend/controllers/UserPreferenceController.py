from flask import request,jsonify
from database import Session
from models.UserPreference import UserPreference

def save_preferences():
    session = Session()
    try:
        data=request.get_json()
        user_id=data.get('user_id')
        peripheral_threshold = data.get('peripheral_threshold')
        distance_threshold = data.get('distance_threshold')
        distance_status = data.get('distance_status')
        peripheral_status = data.get('peripheral_status')
        color_status = data.get('color_status')
        volume_intensity=data.get('volume_intensity')
        text_size=data.get('text_size')
        swap_red_blue=data.get('swap_red_blue')
        swap_yellow_white=data.get('swap_yellow_white')
        swap_green_yellow=data.get('swap_green_yellow')
        print("green ---- yellow",swap_green_yellow,"---",swap_yellow_white)
        if not user_id:
            return jsonify({'Error':'Please provide valid user_id'}),409
        if peripheral_threshold is None:
            peripheral_threshold=10
        if distance_threshold is None:
            distance_threshold = 10
        if volume_intensity is None:
            volume_intensity="medium"
        if text_size is None:
            text_size = "medium"
        if swap_red_blue is None:
            swap_red_blue = "red"
        if swap_yellow_white is None:
            print("NOne value")
            swap_yellow_white = "yellow"
        if swap_green_yellow is None:
            print("None Value")
            swap_green_yellow = "green"
        user=session.query(UserPreference).filter(UserPreference.user_id==user_id).first()
        if user:
            return jsonify({'Error':'User Already exist'}),409
        preference_data=UserPreference(user_id,peripheral_threshold,distance_threshold,distance_status,peripheral_status,color_status,
        volume_intensity,text_size,swap_red_blue,swap_green_yellow,swap_yellow_white)

        session.add(preference_data)
        session.commit()
        return jsonify({'message':'Preferences saved successfully'}),200
    except Exception as e:
        session.rollback()
        return jsonify({'Error':str(e)}),500
    finally:
        session.close()

def get_preference(id):
    session = Session()
    try:
        pref_data=session.query(UserPreference).filter(UserPreference.user_id==id).first()
        if not pref_data:
            return jsonify({"Error":"User does not exist"}),404
        data = {
            'pre_id': pref_data.pre_id,
            'user_id': pref_data.user_id,
            'peripheral_threshold': pref_data.peripheral_threshold,
            'distance_threshold': pref_data.distance_threshold,
            'distance_status': pref_data.distance_status,
            'peripheral_status': pref_data.peripheral_status,
            'color_status': pref_data.color_status,
            'volume_intensity':pref_data.volume_intensity,
            'text_size':pref_data.text_size,
            'swap_red_blue':pref_data.swap_red_blue,
            'swap_green_yellow': pref_data.swap_green_yellow,
            'swap_yellow_white': pref_data.swap_yellow_white
        }
        return jsonify({"message":data}),200
    except Exception as e:
        session.rollback()
        return jsonify({'Error': str(e)}), 500
    finally:
        session.close()

def update_preferences(id):
    session = Session()
    try:
        data=request.get_json()

        peripheral_threshold = data.get('peripheral_threshold')
        distance_threshold = data.get('distance_threshold')
        distance_status = data.get('distance_status')
        peripheral_status = data.get('peripheral_status')
        color_status = data.get('color_status')
        volume_intensity=data.get('volume_intensity')
        text_size=data.get('text_size')
        swap_red_blue=data.get('swap_red_blue')
        swap_yellow_white = data.get('swap_yellow_white')
        swap_green_yellow= data.get('swap_green_yellow')
        user_data=session.query(UserPreference).filter(UserPreference.user_id==id).first()
        if not user_data:
            return jsonify({"message":"User id doesnot exist"}),201
        user_data.user_id=id
        user_data.peripheral_threshold=peripheral_threshold
        user_data.distance_threshold=distance_threshold
        user_data.distance_status=distance_status
        user_data.peripheral_status=peripheral_status
        user_data.color_status=color_status
        user_data.volume_intensity=volume_intensity
        user_data.text_size=text_size
        user_data.swap_red_blue=swap_red_blue
        user_data.swap_green_yellow=swap_green_yellow
        user_data.swap_yellow_white=swap_yellow_white
        session.commit()
        return jsonify({"message":"User Preferences updated successfully"}),200
    except Exception as e:
        session.rollback()
        return jsonify({'Error------': str(e)}), 500
    finally:
        session.close()