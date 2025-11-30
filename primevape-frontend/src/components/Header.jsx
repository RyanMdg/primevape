import { Link, useNavigate } from "react-router-dom";
import {
  FiShoppingCart,
  FiUser,
  FiSearch,
  FiMenu,
  FiX,
  FiLogOut,
} from "react-icons/fi";
import { useState } from "react";
import { useAuth } from "../context/AuthContext";

function Header({ cartCount }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    setUserMenuOpen(false);
    navigate("/");
  };

  return (
    <header className="header">
      <div className="container">
        <nav className="nav">
          <Link to="/" className="logo">
            PRIMEVAPE
          </Link>

          <ul className="nav-links">
            <li>
              <Link to="/">HOME</Link>
            </li>
            <li>
              <Link to="/products">SHOP</Link>
            </li>
            {/* <li><Link to="/products?category=pods">PODS</Link></li>
            <li><Link to="/products?category=liquids">E-LIQUIDS</Link></li>
            <li><Link to="/products?category=accessories">ACCESSORIES</Link></li> */}
          </ul>

          <div className="nav-icons">
            <FiSearch className="nav-icon" />

            <div
              className="user-menu-container"
              style={{ position: "relative" }}
            >
              {isAuthenticated ? (
                <>
                  <FiUser
                    className="nav-icon"
                    onClick={() => setUserMenuOpen(!userMenuOpen)}
                    style={{ cursor: "pointer" }}
                  />
                  {userMenuOpen && (
                    <div className="user-dropdown">
                      <div
                        style={{
                          padding: "0.75rem 1rem",
                          borderBottom: "1px solid var(--gray-light)",
                        }}
                      >
                        <div style={{ fontWeight: 600 }}>
                          {user?.username || "User"}
                        </div>
                        <div
                          style={{
                            fontSize: "0.75rem",
                            color: "var(--gray-medium)",
                          }}
                        >
                          {user?.email}
                        </div>
                      </div>
                      <button onClick={handleLogout} className="dropdown-item">
                        <FiLogOut /> Logout
                      </button>
                    </div>
                  )}
                </>
              ) : (
                <Link to="/login">
                  <FiUser className="nav-icon" />
                </Link>
              )}
            </div>

            <Link to="/cart" style={{ position: "relative", color: "inherit" }}>
              <FiShoppingCart className="nav-icon" />
              {cartCount > 0 && <span className="cart-badge">{cartCount}</span>}
            </Link>
            <div
              className="mobile-menu-icon"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? <FiX /> : <FiMenu />}
            </div>
          </div>
        </nav>

        {mobileMenuOpen && (
          <div className="mobile-menu">
            <Link to="/" onClick={() => setMobileMenuOpen(false)}>
              HOME
            </Link>
            <Link to="/products" onClick={() => setMobileMenuOpen(false)}>
              SHOP
            </Link>
            <Link
              to="/products?category=pods"
              onClick={() => setMobileMenuOpen(false)}
            >
              PODS
            </Link>
            <Link
              to="/products?category=liquids"
              onClick={() => setMobileMenuOpen(false)}
            >
              E-LIQUIDS
            </Link>
            <Link
              to="/products?category=accessories"
              onClick={() => setMobileMenuOpen(false)}
            >
              ACCESSORIES
            </Link>
            {!isAuthenticated && (
              <>
                <Link to="/login" onClick={() => setMobileMenuOpen(false)}>
                  LOGIN
                </Link>
                <Link to="/register" onClick={() => setMobileMenuOpen(false)}>
                  REGISTER
                </Link>
              </>
            )}
            {isAuthenticated && (
              <a
                onClick={() => {
                  handleLogout();
                  setMobileMenuOpen(false);
                }}
                style={{ cursor: "pointer" }}
              >
                LOGOUT
              </a>
            )}
          </div>
        )}
      </div>
    </header>
  );
}

export default Header;
