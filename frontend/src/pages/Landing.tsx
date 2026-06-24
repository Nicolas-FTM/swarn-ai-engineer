import React from 'react';
import { useNavigate } from 'react-router-dom';

const Landing: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-pink-50 to-rose-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">Sweet Haven Bakery</h1>
            </div>
            <button
              onClick={() => navigate('/login')}
              className="bg-amber-600 text-white px-4 py-2 rounded-md hover:bg-amber-700 transition-colors"
            >
              Sign In
            </button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-5xl font-extrabold text-gray-900 sm:text-6xl">
            <span className="block">Handcrafted Delights</span>
            <span className="block text-amber-600">Just for You</span>
          </h2>
          <p className="mt-6 max-w-2xl mx-auto text-xl text-gray-600">
            Experience the art of baking with our artisanal pastries, cakes, and breads, made daily with the finest ingredients and love.
          </p>
          <div className="mt-10 flex justify-center">
            <button
              onClick={() => navigate('/login')}
              className="bg-amber-600 text-white px-8 py-3 text-lg font-medium rounded-full hover:bg-amber-700 transition-all transform hover:scale-105 shadow-lg"
            >
              Visit Our Chat Assistant
            </button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h3 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
              Our Specialties
            </h3>
            <p className="mt-4 max-w-2xl mx-auto text-xl text-gray-600">
              Discover our signature creations that have won the hearts of customers worldwide
            </p>
          </div>

          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            <div className="bg-amber-50 p-8 rounded-lg text-center hover:bg-amber-100 transition-colors">
              <div className="text-4xl mb-4">🍰</div>
              <h4 className="text-xl font-semibold text-gray-900 mb-2">Artisan Pastries</h4>
              <p className="text-gray-600">Flaky, buttery pastries filled with premium fillings, baked to perfection daily.</p>
            </div>

            <div className="bg-pink-50 p-8 rounded-lg text-center hover:bg-pink-100 transition-colors">
              <div className="text-4xl mb-4">🎂</div>
              <h4 className="text-xl font-semibold text-gray-900 mb-2">Custom Cakes</h4>
              <p className="text-gray-600">Personalized cakes for birthdays, weddings, and special occasions, designed to impress.</p>
            </div>

            <div className="bg-rose-50 p-8 rounded-lg text-center hover:bg-rose-100 transition-colors">
              <div className="text-4xl mb-4">🍞</div>
              <h4 className="text-xl font-semibold text-gray-900 mb-2">Fresh Breads</h4>
              <p className="text-gray-600">Hand-shaped sourdoughs, rustic loaves, and daily specials baked with traditional methods.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h3 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
            What Our Customers Say
          </h3>
          <div className="mt-10 grid grid-cols-1 gap-6">
            <blockquote className="bg-white p-8 rounded-lg shadow-md">
              <p className="text-lg text-gray-700 italic">
                "The croissants at Sweet Haven Bakery are the best I've ever tasted. The attention to detail in every pastry is truly remarkable."
              </p>
              <footer className="mt-4 text-gray-600">— Sarah M., Regular Customer</footer>
            </blockquote>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-amber-600 text-white">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h3 className="text-3xl font-extrabold mb-6">Ready to Experience Our Delights?</h3>
          <p className="text-xl mb-8 opacity-90">
            Our friendly chat assistant is available 24/7 to answer all your questions about our products and services.
          </p>
          <button
            onClick={() => navigate('/login')}
            className="bg-white text-amber-600 px-8 py-3 text-lg font-medium rounded-full hover:bg-gray-100 transition-all transform hover:scale-105 shadow-lg"
          >
            Chat with Our Assistant
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p>&copy; 2026 Sweet Haven Bakery. All rights reserved.</p>
          <p className="mt-2 text-sm text-gray-400">Handcrafted with love in every bite</p>
        </div>
      </footer>
    </div>
  );
};

export default Landing;