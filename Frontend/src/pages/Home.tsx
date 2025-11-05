import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { 
  Activity, 
  AlertCircle, 
  MapPin, 
  Clock,
  TrendingUp,
  AlertTriangle,
  Droplet,
  Heart
} from "lucide-react";
import { toast } from "sonner";
import { Link } from "react-router-dom";

interface Statistics {
  total_predictions_today: number;
  critical_alerts: number;
  districts_monitored: number;
  average_response_time_hours: number;
}

interface Alert {
  id: number;
  domain: string;
  district: string;
  severity: string;
  message: string;
  probability?: number;
  timeline?: string;
  timestamp: string;
}

const Home = () => {
  const [apiStatus, setApiStatus] = useState<"connected" | "disconnected">("disconnected");
  const [statistics, setStatistics] = useState<Statistics>({
    total_predictions_today: 1247,
    critical_alerts: 12,
    districts_monitored: 36,
    average_response_time_hours: 2.5,
  });
  const [alerts, setAlerts] = useState<Alert[]>([
    {
      id: 1,
      domain: "Infrastructure",
      district: "Mumbai",
      severity: "CRITICAL",
      message: "Water Shortage",
      probability: 87,
      timeline: "3 days",
      timestamp: new Date().toISOString(),
    },
    {
      id: 2,
      domain: "Health",
      district: "Pune",
      severity: "HIGH",
      message: "Hospital ICU Full",
      probability: 92,
      timeline: "Immediate",
      timestamp: new Date().toISOString(),
    },
  ]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAPIStatus();
    fetchDashboardData();
  }, []);

  const checkAPIStatus = async () => {
    try {
      const response = await fetch("https://api.predictivminds.shop/health");
      if (response.ok) {
        setApiStatus("connected");
      }
    } catch (error) {
      setApiStatus("disconnected");
    }
  };

  const fetchDashboardData = async () => {
    try {
      const [statsRes, alertsRes] = await Promise.all([
        fetch("https://api.predictivminds.shop/api/v1/dashboard/statistics"),
        fetch("https://api.predictivminds.shop/api/v1/dashboard/alerts"),
      ]);

      console.log("Statistics Response Status:", statsRes.status);
      console.log("Alerts Response Status:", alertsRes.status);

      if (statsRes.ok) {
        const statsData = await statsRes.json();
        console.log("Statistics API Response:", statsData);
        
        // Update with API data if available
        setStatistics({
          total_predictions_today: statsData.statistics?.total_predictions_today || statsData.total_predictions_today || 1247,
          critical_alerts: statsData.statistics?.critical_alerts || statsData.critical_alerts || 12,
          districts_monitored: statsData.statistics?.districts_monitored || statsData.districts_monitored || 36,
          average_response_time_hours: statsData.statistics?.average_response_time_hours || statsData.average_response_time_hours || 2.5,
        });
      } else {
        console.log("Statistics API failed, using demo data");
      }

      if (alertsRes.ok) {
        const alertsData = await alertsRes.json();
        console.log("Alerts API Response:", alertsData);
        
        if (alertsData.alerts && alertsData.alerts.length > 0) {
          setAlerts(alertsData.alerts);
        } else {
          console.log("No alerts from API, using demo data");
        }
      } else {
        console.log("Alerts API failed, using demo data");
      }
    } catch (error) {
      console.error("Dashboard API Error:", error);
      // Demo data is already set in initial state
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity?.toUpperCase()) {
      case "CRITICAL": return "destructive";
      case "HIGH": return "secondary";
      case "MEDIUM": return "default";
      default: return "outline";
    }
  };

  const getSeverityIcon = (domain: string) => {
    switch (domain?.toLowerCase()) {
      case "infrastructure": return Droplet;
      case "health": return Heart;
      default: return AlertTriangle;
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <Activity className="h-8 w-8 animate-spin mx-auto mb-4" />
          <p className="text-muted-foreground">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="h-16 w-16 rounded-full bg-gradient-to-br from-primary to-health flex items-center justify-center shadow-lg">
            <span className="text-3xl">🏛️</span>
          </div>
          <div>
            <h1 className="text-3xl font-bold text-foreground mb-2">
              PREDICTIVMINDS - AI Governance Platform
            </h1>
            <div className="flex items-center gap-2">
              <span className="text-muted-foreground">API Status:</span>
              <Badge variant={apiStatus === "connected" ? "default" : "destructive"}>
                {apiStatus === "connected" ? "🟢 Connected" : "🔴 Disconnected"}
              </Badge>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Stats - 4 Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="border-l-4 border-l-primary">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Predictions
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-3xl font-bold">{statistics?.total_predictions_today}</p>
                <p className="text-xs text-muted-foreground mt-1">Today</p>
              </div>
              <Activity className="h-8 w-8 text-primary opacity-50" />
            </div>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-destructive">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Alerts
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-3xl font-bold">{statistics?.critical_alerts}</p>
                <p className="text-xs text-muted-foreground mt-1">Critical</p>
              </div>
              <AlertCircle className="h-8 w-8 text-destructive opacity-50" />
            </div>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-blue-500">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Districts
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-3xl font-bold">{statistics?.districts_monitored}</p>
                <p className="text-xs text-muted-foreground mt-1">Monitored</p>
              </div>
              <MapPin className="h-8 w-8 text-blue-500 opacity-50" />
            </div>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-green-500">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Response Time
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-3xl font-bold">{statistics?.average_response_time_hours}h</p>
                <p className="text-xs text-muted-foreground mt-1">Average</p>
              </div>
              <Clock className="h-8 w-8 text-green-500 opacity-50" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Critical Alerts - Top 5 */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <AlertCircle className="h-5 w-5 text-destructive" />
            🚨 CRITICAL ALERTS (Top 5)
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {alerts.length === 0 ? (
            <p className="text-center text-muted-foreground py-8">
              No critical alerts at this time
            </p>
          ) : (
            alerts.slice(0, 5).map((alert) => {
              const Icon = getSeverityIcon(alert.domain);
              return (
                <div
                  key={alert.id}
                  className="border rounded-lg p-4 hover:bg-muted/50 transition-colors"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex items-start gap-3 flex-1">
                      <Icon className="h-5 w-5 mt-1 text-destructive" />
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <Badge variant={getSeverityColor(alert.severity)}>
                            {alert.severity}
                          </Badge>
                          <h4 className="font-semibold">
                            {alert.message} - {alert.district}
                          </h4>
                        </div>
                        <div className="text-sm text-muted-foreground space-y-1">
                          {alert.probability && (
                            <p>Probability: {alert.probability}%</p>
                          )}
                          {alert.timeline && (
                            <p>Timeline: {alert.timeline}</p>
                          )}
                          <p>Domain: {alert.domain}</p>
                        </div>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <Button size="sm" variant="outline" asChild>
                        <Link to="/predictions">View Details</Link>
                      </Button>
                      <Button size="sm">Take Action</Button>
                    </div>
                  </div>
                </div>
              );
            })
          )}
        </CardContent>
      </Card>

      {/* Trend Chart Placeholder */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            📈 TREND CHART (Last 7 days)
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-64 flex items-center justify-center bg-muted/20 rounded-lg border-2 border-dashed">
            <div className="text-center">
              <TrendingUp className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
              <p className="text-muted-foreground">
                Prediction trends visualization
              </p>
              <p className="text-sm text-muted-foreground mt-2">
                Shows demand, crisis, and priority trends over time
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Button size="lg" className="h-20" asChild>
          <Link to="/predictions">
            <div className="text-center">
              <p className="font-semibold">Make Prediction</p>
              <p className="text-xs opacity-90">Demand, Crisis, Priority</p>
            </div>
          </Link>
        </Button>
        <Button size="lg" variant="outline" className="h-20" asChild>
          <Link to="/data-management">
            <div className="text-center">
              <p className="font-semibold">Upload Data</p>
              <p className="text-xs opacity-90">Excel files for analysis</p>
            </div>
          </Link>
        </Button>
        <Button size="lg" variant="outline" className="h-20" asChild>
          <Link to="/reports">
            <div className="text-center">
              <p className="font-semibold">View Reports</p>
              <p className="text-xs opacity-90">Analytics & trends</p>
            </div>
          </Link>
        </Button>
      </div>
    </div>
  );
};

export default Home;
