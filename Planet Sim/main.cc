#include <SFML/Graphics.hpp>
#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include <deque>
#include <iomanip>
#include <sstream>

using namespace std;
using namespace sf;

const int WIDTH = 1920;
const int HEIGHT = 1080;

constexpr double G = 6.67428e-11;
constexpr double AU = 149.6e6 * 1000.0;
constexpr double BASE_TIMESTEP = 3600.0;
constexpr double INITIAL_SCALE = 60.0 / AU;
constexpr double FOCUS_SCALE = INITIAL_SCALE * 30.0;
constexpr double LERP_FACTOR = 0.05;

Color dimColor(const Color& color, float factor = 0.4f) {
	return Color(static_cast<Uint8>(color.r * factor), static_cast<Uint8>(color.g * factor), static_cast<Uint8>(color.b * factor));
}

struct PlanetData {
	string name;
	Color color;
	double mass;
	double radius;
	double dist_au;
	double y_vel;
};

vector<PlanetData> PLANET_DATA = {
	{"Mercury", {255, 204, 153}, 0.33e24, 2439, 0.4, 47.4},
	{"Venus",   {255, 153, 153}, 4.87e24, 6051, 0.7, 35.0},
	{"Earth",   {0, 102, 255},   5.97e24, 6371, 1.0, 29.8},
	{"Mars",    {255, 102, 0},   0.642e24, 3389, 1.5, 24.0},
	{"Jupiter", {204, 153, 0},   1898e24, 69911, 5.2, 13.1},
	{"Saturn",  {255, 255, 204}, 568e24, 58232, 9.5, 9.7},
	{"Uranus",  {0, 153, 255},   86.8e24, 25362, 19.8, 6.8},
	{"Neptune", {102, 153, 255}, 102e24, 24622, 30.0, 5.4},
};

class Planet {
public:
	Vector2<double> pos, vel, acc;
	double radius_real, mass;
	Color color, dimmed_color;
	string name;
	bool is_sun = false;
	double distance_to_sun = 0.0;
	deque<Vector2<double>> orbit_trail;
	vector<Vector2<double>> full_orbit;
	bool has_completed_orbit = false;
	double last_y_pos = 0.0;

	Planet(double x, double y, double r_km, Color c, double m, string n, double y_vel_kms = 0.0)
		: pos(x, y), radius_real(r_km * 1000.0), mass(m), color(c), name(n),
		  vel(0.0, y_vel_kms * 1000.0), acc(0.0, 0.0), dimmed_color(dimColor(c)), last_y_pos(y) {}

	void calculate_forces(const vector<Planet>& planets) {
		Vector2<double> total_force(0.0, 0.0);
		for (const auto& other : planets) {
			if (&other == this) continue;
			Vector2<double> delta = other.pos - pos;
			double dist = sqrt(delta.x * delta.x + delta.y * delta.y);
			if (other.is_sun) distance_to_sun = dist;
			double force_mag = G * mass * other.mass / (dist * dist);
			total_force += (delta / dist) * force_mag;
		}
		acc = total_force / mass;
	}

	void update_position_verlet(double timestep) {
		pos += vel * timestep + 0.5 * acc * (timestep * timestep);
		orbit_trail.push_back(pos);
		if (orbit_trail.size() > 150) {
			orbit_trail.pop_front();
		}

		if (!is_sun && !has_completed_orbit) {
			if (last_y_pos < 0 && pos.y >= 0 && pos.x > 0) {
				has_completed_orbit = true;
			}
			full_orbit.push_back(pos);
		}
		last_y_pos = pos.y;
	}


	void draw(RenderWindow& window, double scale, const Vector2<double>& camera, bool show_info, Font& font) {
		Vector2f screen_pos((pos.x - camera.x) * scale + WIDTH / 2.0, (pos.y - camera.y) * scale + HEIGHT / 2.0);
		float radius_scaled = max(2.0, radius_real * scale);

		if (full_orbit.size() > 2) {
			VertexArray lines(LineStrip);
			for (const auto& p : full_orbit) {
				lines.append(Vertex({(float)((p.x - camera.x) * scale + WIDTH / 2.0), (float)((p.y - camera.y) * scale + HEIGHT / 2.0)}, dimmed_color));
			}
			window.draw(lines);
		}
		if (orbit_trail.size() > 2) {
			VertexArray lines(LineStrip);
			for (const auto& p : orbit_trail) {
				lines.append(Vertex({(float)((p.x - camera.x) * scale + WIDTH / 2.0), (float)((p.y - camera.y) * scale + HEIGHT / 2.0)}, color));
			}
			window.draw(lines);
		}

		CircleShape circle(radius_scaled);
		circle.setFillColor(color);
		circle.setOrigin(radius_scaled, radius_scaled);
		circle.setPosition(screen_pos);
		window.draw(circle);

		if (!is_sun && show_info) {
			Text name_text(name, font, 16);
			name_text.setFillColor(Color::White);
			FloatRect text_rect = name_text.getLocalBounds();
			name_text.setOrigin(text_rect.left + text_rect.width / 2.0f, text_rect.top + text_rect.height / 2.0f);
			name_text.setPosition(screen_pos.x, screen_pos.y - radius_scaled - 12);
			window.draw(name_text);

			stringstream ss;
			ss << fixed << setprecision(2) << distance_to_sun / AU << " AU";
			Text dist_text(ss.str(), font, 14);
			dist_text.setFillColor(Color::White);
			text_rect = dist_text.getLocalBounds();
			dist_text.setOrigin(text_rect.left + text_rect.width / 2.0f, text_rect.top + text_rect.height / 2.0f);
			dist_text.setPosition(screen_pos.x, screen_pos.y + radius_scaled + 10);
			window.draw(dist_text);
		}
	}
};

class UI {
private:
	struct Button { RectangleShape rect; Text text; Planet* planet; };
	vector<Button> buttons;
	Color bg_color = {40, 40, 40}, hover_color = {70, 70, 70};
public:
	UI(vector<Planet>& planets, Font& font) {
		float panel_width = 200, panel_x = WIDTH - panel_width - 10, y_offset = 10;
		for (auto& planet : planets) {
			if (planet.is_sun) continue;
			Button btn;
			btn.planet = &planet;
			btn.rect.setSize({panel_width, 30.f});
			btn.rect.setPosition(panel_x, y_offset);
			btn.text.setFont(font);
			btn.text.setString(planet.name);
			btn.text.setCharacterSize(16);
			FloatRect textRect = btn.text.getLocalBounds();
			btn.text.setOrigin(textRect.left + textRect.width / 2.0f, textRect.top + textRect.height / 2.0f);
			btn.text.setPosition(panel_x + panel_width / 2.0f, y_offset + 15.f);
			buttons.push_back(btn);
			y_offset += 35;
		}
	}
	void draw(RenderWindow& window) {
		Vector2f mousePos = static_cast<Vector2f>(Mouse::getPosition(window));
		for (auto& btn : buttons) {
			btn.rect.setFillColor(btn.rect.getGlobalBounds().contains(mousePos) ? hover_color : bg_color);
			window.draw(btn.rect);
			window.draw(btn.text);
		}
	}
	Planet* handleClick(Vector2i mousePos) {
		for (const auto& btn : buttons) {
			if (btn.rect.getGlobalBounds().contains(static_cast<Vector2f>(mousePos))) return btn.planet;
		}
		return nullptr;
	}
};

int main() {
	RenderWindow window(VideoMode(WIDTH, HEIGHT), "Planet Simulation", Style::Fullscreen);
	window.setFramerateLimit(300);
	Clock clock;

	Font font;
	if (!font.loadFromFile("C:/Windows/Fonts/consola.ttf") && !font.loadFromFile("C:/Windows/Fonts/arial.ttf")) {
		cerr << "Error: Failed to load system fonts (Consolas or Arial)!" << endl;
		return -1;
	}
	Text fpsText("", font, 20);
	fpsText.setFillColor(Color::White);

	double scale = INITIAL_SCALE, time_multiplier = 1.0;
	bool show_info = true;
	Vector2<double> camera_pos(0.0, 0.0);
	Planet* camera_target = nullptr;
	const double CAMERA_SPEED = 20.0;
	
	vector<Planet> planets;
	planets.emplace_back(0, 0, 696340, Color(255, 204, 0), 1.98892e30, "Sun").is_sun = true;
	for (const auto& data : PLANET_DATA) {
		planets.emplace_back(-data.dist_au * AU, 0, data.radius, data.color, data.mass, data.name, data.y_vel);
	}
	UI ui(planets, font);
	for (auto& p : planets) {
		if (!p.is_sun) p.calculate_forces(planets);
	}

	while (window.isOpen()) {
		Time elapsed = clock.restart();
		double timestep = BASE_TIMESTEP * time_multiplier;
		Event event;

		while (window.pollEvent(event)) {
			if (event.type == Event::Closed) window.close();
			if (event.type == Event::MouseButtonPressed && event.mouseButton.button == Mouse::Left) {
				if (Planet* clicked = ui.handleClick({event.mouseButton.x, event.mouseButton.y})) camera_target = clicked;
			}
			if (event.type == Event::KeyPressed) {
				bool user_interrupted = true;
				if (event.key.code == Keyboard::Escape) window.close();
				else if (event.key.code == Keyboard::Add || event.key.code == Keyboard::Equal) scale *= 1.5;
				else if (event.key.code == Keyboard::Subtract || event.key.code == Keyboard::Hyphen) scale /= 1.5;
				else if (event.key.code == Keyboard::Up) time_multiplier *= 1.5;
				else if (event.key.code == Keyboard::Down) time_multiplier = max(0.1, time_multiplier / 1.5);
				else if (event.key.code == Keyboard::I) show_info = !show_info;
				else if (event.key.code == Keyboard::R) { camera_pos = {0.0, 0.0}; scale = INITIAL_SCALE; }
				else user_interrupted = false;
				if (user_interrupted) camera_target = nullptr;
			}
		}

		double move_amount = CAMERA_SPEED / scale;
		bool user_moved = false;
		if (Keyboard::isKeyPressed(Keyboard::W)) { camera_pos.y -= move_amount; user_moved = true; }
		if (Keyboard::isKeyPressed(Keyboard::S)) { camera_pos.y += move_amount; user_moved = true; }
		if (Keyboard::isKeyPressed(Keyboard::A)) { camera_pos.x -= move_amount; user_moved = true; }
		if (Keyboard::isKeyPressed(Keyboard::D)) { camera_pos.x += move_amount; user_moved = true; }
		if (user_moved) camera_target = nullptr;

		if (camera_target) {
			Vector2<double> target_pos = camera_target->pos;
			camera_pos.x += (target_pos.x - camera_pos.x) * LERP_FACTOR;
			camera_pos.y += (target_pos.y - camera_pos.y) * LERP_FACTOR;
			scale += (FOCUS_SCALE - scale) * LERP_FACTOR;
			if (abs(camera_pos.x - target_pos.x) < 1e6 && abs(scale - FOCUS_SCALE) < 1e-12) camera_target = nullptr;
		}

		vector<Vector2<double>> old_accs;
		for(const auto& p : planets) old_accs.push_back(p.acc);

		for (auto& p : planets) if (!p.is_sun) p.update_position_verlet(timestep);
		for (auto& p : planets) if (!p.is_sun) p.calculate_forces(planets);
		for (size_t i = 0; i < planets.size(); ++i) {
			if (!planets[i].is_sun) planets[i].vel += 0.5 * (old_accs[i] + planets[i].acc) * timestep;
		}

		window.clear({15, 15, 15});
		for (auto& p : planets) p.draw(window, scale, camera_pos, show_info, font);
		ui.draw(window);

		stringstream info_ss;
		info_ss << "Zoom: " << fixed << setprecision(1) << scale / INITIAL_SCALE << "x  | +/- to change\n"
				<< "Time: " << time_multiplier << "x | UP/DOWN to change\n"
				<< "Info: " << (show_info ? "ON" : "OFF") << " | Press 'I' to toggle\n"
				<< "Move: WASD | Reset: R | Focus: Click list";
		Text control_text(info_ss.str(), font, 16);
		control_text.setPosition(10, 10);
		window.draw(control_text);

		stringstream fps_ss;
		fps_ss << "FPS: " << static_cast<int>(1.f / elapsed.asSeconds());
		fpsText.setString(fps_ss.str());
		fpsText.setPosition(WIDTH - fpsText.getGlobalBounds().width - 10, HEIGHT - fpsText.getGlobalBounds().height - 15);
		window.draw(fpsText);
		
		window.display();
	}
	return 0;
}