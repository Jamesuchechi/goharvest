import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Navbar from './components/layout/Navbar.jsx';
import Sidebar from './components/layout/Sidebar.jsx';
import Footer from './components/layout/Footer.jsx';
import Dashboard from './pages/Dashboard.jsx';
import JobList from './pages/JobList.jsx';
import JobDetail from './pages/JobDetail.jsx';
import ResultsBrowser from './pages/ResultsBrowser.jsx';
import TechExplorer from './pages/TechExplorer.jsx';
import BatchProcessor from './pages/BatchProcessor.jsx';
import VisualInspector from './pages/VisualInspector.jsx';
import ComparisonView from './pages/ComparisonView.jsx';
import ComponentLibrary from './pages/ComponentLibrary.jsx';
import Analytics from './pages/Analytics.jsx';
import Settings from './pages/Settings.jsx';
import Docs from './pages/Docs.jsx';
import { AuthProvider } from './contexts/AuthContext.jsx';
import { ThemeProvider } from './contexts/ThemeContext.jsx';

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <ThemeProvider>
          <div className="layout">
            <Navbar />
            <div className="main">
              <Sidebar />
              <div className="content">
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/jobs" element={<JobList />} />
                  <Route path="/jobs/:id" element={<JobDetail />} />
                  <Route path="/results" element={<ResultsBrowser />} />
                  <Route path="/tech-explorer" element={<TechExplorer />} />
                  <Route path="/batch" element={<BatchProcessor />} />
                  <Route path="/visual/:id" element={<VisualInspector />} />
                  <Route path="/compare" element={<ComparisonView />} />
                  <Route path="/components" element={<ComponentLibrary />} />
                  <Route path="/analytics" element={<Analytics />} />
                  <Route path="/settings" element={<Settings />} />
                  <Route path="/docs" element={<Docs />} />
                </Routes>
              </div>
            </div>
            <Footer />
          </div>
        </ThemeProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}
