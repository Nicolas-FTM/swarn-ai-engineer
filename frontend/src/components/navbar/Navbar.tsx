import styles from "./Navbar.module.css";

interface User {
  email: string
}

interface NavbarProps {
  isAuthenticated: boolean
  user?: User | null
}

function Navbar({ isAuthenticated, user }: NavbarProps) {
  return (
    <nav className={styles["navbar"]}>
      <div className={styles["navbar-content"]}>
        <h1 className={styles["logo"]}>Swarn RAG Chatbot</h1>

        <div className={styles["navbar-actions"]}>
          {isAuthenticated && user && (
            <span className={styles["user-info"]}>{user.email}</span>
          )}
        </div>
      </div>
    </nav>
  )
}

export default Navbar