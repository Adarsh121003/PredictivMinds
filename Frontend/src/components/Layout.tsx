import { ReactNode } from "react";
import { Link, useLocation } from "react-router-dom";
import { cn } from "@/lib/utils";
import { 
  Home,
  Activity, 
  BarChart3, 
  FolderUp, 
  Shield,
  Menu
} from "lucide-react";

interface LayoutProps {
  children: ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  const location = useLocation();

  const navItems = [
    { path: "/", label: "🏠 Home Dashboard", icon: Home },
    { path: "/predictions", label: "🔮 Predictions", icon: Activity },
    { path: "/data-management", label: "📂 Data Management", icon: FolderUp },
    { path: "/reports", label: "📊 Reports & Analytics", icon: BarChart3 },
    { path: "/privacy-compliance", label: "🔒 Compliance", icon: Shield },
  ];

  return (
    <div className="min-h-screen bg-background flex">
      {/* Sidebar */}
      <aside className="w-64 bg-card border-r border-border flex flex-col">
        <div className="p-6 border-b border-border bg-primary text-primary-foreground">
          <div className="flex items-center gap-3 mb-2">
            <img 
              src="/favicon.ico" 
              alt="Logo" 
              className="h-8 w-8"
              onError={(e) => {
                e.currentTarget.style.display = 'none';
              }}
            />
            <Activity className="h-8 w-8" />
            <h1 className="text-xl font-bold">PREDICTIVMINDS</h1>
          </div>
          <p className="text-xs opacity-90">AI Governance Platform</p>
        </div>
        
        <nav className="flex-1 p-4 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            
            return (
              <Link
                key={item.path}
                to={item.path}
                className={cn(
                  "flex items-center gap-3 px-4 py-3 rounded-lg transition-colors",
                  isActive 
                    ? "bg-primary text-primary-foreground" 
                    : "text-muted-foreground hover:bg-muted hover:text-foreground"
                )}
              >
                <Icon className="h-5 w-5" />
                <span className="text-sm font-medium">{item.label}</span>
              </Link>
            );
          })}
        </nav>
        
        <div className="p-4 border-t border-border">
          <div className="flex items-center gap-2 px-4 py-2">
            <div className="h-2 w-2 rounded-full bg-health animate-pulse" />
            <span className="text-xs text-muted-foreground">System Online</span>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        <div className="p-8">
          {children}
        </div>
      </main>
    </div>
  );
};

export default Layout;
