from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

OUTFITS = {
    "Female": {
        "Traditional": {
            "Indian": ["Cotton Kurti Set", "Anarkali Suit", "Saree", "Salwar Kameez", "Lehenga"],
            "Korean": ["Korean Traditional Dress", "Hanbok Inspired Outfit"]
        },
        "Casual": {
            "Indian": ["Kurti with Palazzo", "Cotton Kurti", "Ethnic Co-ord Set"],
            "Korean": ["Oversized Shirt and Jeans", "Korean Cardigan Look", "Casual Co-ord"]
        },
        "Formal": {
            "Indian": ["Formal Kurti Set", "Straight Cut Suit"],
            "Korean": ["Blazer and Trousers", "Formal Midi Dress"]
        },
        "Trendy": {
            "Indian": ["Indo Western Dress", "Sharara Set"],
            "Korean": ["Korean Layered Dress", "Korean Streetwear"]
        }
    },
    "Male": {
        "Traditional": {
            "Indian": ["Kurta Pajama", "Sherwani", "Dhoti Kurta"],
            "Korean": ["Korean Hanbok"]
        },
        "Casual": {
            "Indian": ["Casual Kurta", "Shirt and Trousers"],
            "Korean": ["Oversized Shirt and Pants", "Korean Casual Outfit"]
        },
        "Formal": {
            "Indian": ["Formal Shirt and Trousers", "Nehru Jacket Outfit"],
            "Korean": ["Korean Formal Suit", "Blazer and Trousers"]
        },
        "Trendy": {
            "Indian": ["Indo Western Kurta", "Trendy Jacket Outfit"],
            "Korean": ["Korean Streetwear", "Layered Korean Outfit"]
        }
    }
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json() or {}

    gender = data.get("gender", "Female")
    style = data.get("style", "Indian")
    category = data.get("category", "Traditional")
    color = data.get("color", "Pink")
    weather = data.get("weather", "Summer")
    occasion = data.get("occasion", "College")
    budget = data.get("budget", "Below ₹500")

    gender_data = OUTFITS.get(gender, OUTFITS["Female"])
    category_data = gender_data.get(category, gender_data["Traditional"])

    if style == "Both":
        outfit_names = category_data["Indian"] + category_data["Korean"]
    else:
        outfit_names = category_data.get(style, category_data["Indian"])

    recommendations = []

    for name in outfit_names:
        if weather == "Summer":
            accessories = "Light accessories and comfortable footwear"
        elif weather == "Winter":
            accessories = "Matching jacket, scarf and footwear"
        else:
            accessories = "Minimal accessories and comfortable footwear"

        recommendations.append({
            "name": name if color == "Any Colour" else f"{color} {name}",
            "gender": gender,
            "style": style,
            "category": category,
            "color": color,
            "weather": weather,
            "occasion": occasion,
            "budget": budget,
            "accessories": accessories
        })

    return jsonify({"outfits": recommendations})


if __name__ == "__main__":
    app.run(debug=True)