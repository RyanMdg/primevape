import { Link } from "react-router-dom";
import { FiFacebook, FiInstagram, FiTwitter } from "react-icons/fi";

function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-section">
            <h3>PRIMEVAPE</h3>
            <p>
              Your premium destination for quality vaping products. Elevate your
              experience.
            </p>
          </div>

          <div className="footer-section">
            <h3>Quick Links</h3>
            <ul>
              <li>
                <Link to="/products">Shop All</Link>
              </li>
              <li>
                <Link to="/products?category=pods">Vape Pods</Link>
              </li>
              <li>
                <Link to="/products?category=liquids">E-Liquids</Link>
              </li>
              <li>
                <Link to="/products?category=accessories">Accessories</Link>
              </li>
            </ul>
          </div>

          <div className="footer-section">
            <h3>Customer Service</h3>
            <ul>
              <li>
                <a href="#">Contact Us</a>
              </li>
              <li>
                <a href="#">Shipping Info</a>
              </li>
              <li>
                <a href="#">Returns</a>
              </li>
              <li>
                <a href="#">FAQ</a>
              </li>
            </ul>
          </div>

          <div className="footer-section">
            <h3>Legal</h3>
            <ul>
              <li>
                <a href="#">Terms & Conditions</a>
              </li>
              <li>
                <a href="#">Privacy Policy</a>
              </li>
              <li>
                <a href="#">Age Verification</a>
              </li>
            </ul>
          </div>

          <div className="footer-section">
            <h3>Follow Us</h3>
            <div style={{ display: "flex", gap: "1rem", fontSize: "1.5rem" }}>
              <FiFacebook style={{ cursor: "pointer" }} />
              <FiInstagram style={{ cursor: "pointer" }} />
              <FiTwitter style={{ cursor: "pointer" }} />
            </div>
          </div>
        </div>

        <div className="footer-bottom">
          <p>
            &copy; 2024 PrimeVape. All rights reserved.By Fantastic 4 with
            silver surfer! | Age 21+ Only
          </p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
