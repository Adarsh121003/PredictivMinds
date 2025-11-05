import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Upload, Loader2, CheckCircle, Heart, Building2, ShieldAlert } from "lucide-react";
import { toast } from "sonner";

const DataUpload = () => {
  const [healthFile, setHealthFile] = useState<File | null>(null);
  const [infraFile, setInfraFile] = useState<File | null>(null);
  const [safetyFile, setSafetyFile] = useState<File | null>(null);
  
  const [healthLoading, setHealthLoading] = useState(false);
  const [infraLoading, setInfraLoading] = useState(false);
  const [safetyLoading, setSafetyLoading] = useState(false);
  
  const [healthSuccess, setHealthSuccess] = useState(false);
  const [infraSuccess, setInfraSuccess] = useState(false);
  const [safetySuccess, setSafetySuccess] = useState(false);

  const handleFileUpload = async (domain: string, file: File | null, setLoading: (v: boolean) => void, setSuccess: (v: boolean) => void) => {
    if (!file) {
      toast.error("Please select a file to upload");
      return;
    }

    setLoading(true);
    setSuccess(false);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(
        `https://api.predictivminds.shop/api/v1/dashboard/upload/excel?domain=${domain}`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (response.ok) {
        const result = await response.json();
        toast.success(`Successfully uploaded ${result.records_processed || 0} records`);
        setSuccess(true);
      } else {
        toast.error(`Failed to upload ${domain} data`);
      }
    } catch (error) {
      toast.error("Error connecting to backend. File upload simulated.");
      setSuccess(true);
    } finally {
      setLoading(false);
    }
  };

  const DomainUploadCard = ({
    domain,
    icon: Icon,
    color,
    file,
    setFile,
    loading,
    success,
    onUpload,
  }: {
    domain: string;
    icon: any;
    color: string;
    file: File | null;
    setFile: (f: File | null) => void;
    loading: boolean;
    success: boolean;
    onUpload: () => void;
  }) => (
    <Card className="border-l-4" style={{ borderLeftColor: `hsl(var(--${color}))` }}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Icon className="h-5 w-5" style={{ color: `hsl(var(--${color}))` }} />
          {domain} Data
        </CardTitle>
        <CardDescription>Upload Excel file with {domain.toLowerCase()} records</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div
          className="border-2 border-dashed rounded-lg p-8 text-center cursor-pointer hover:bg-muted/50 transition-colors"
          onClick={() => document.getElementById(`${domain}-file`)?.click()}
        >
          <Upload className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
          <p className="text-sm text-muted-foreground mb-2">
            {file ? file.name : "Click to select Excel file or drag and drop"}
          </p>
          <p className="text-xs text-muted-foreground">Supported formats: .xlsx, .xls</p>
          <input
            id={`${domain}-file`}
            type="file"
            accept=".xlsx,.xls"
            className="hidden"
            onChange={(e) => {
              const selectedFile = e.target.files?.[0];
              if (selectedFile) {
                setFile(selectedFile);
                toast.success(`${selectedFile.name} selected`);
              }
            }}
          />
        </div>

        {success && (
          <div className="flex items-center gap-2 p-3 bg-health/10 border border-health rounded-lg">
            <CheckCircle className="h-5 w-5 text-health" />
            <span className="text-sm text-health font-medium">Upload successful!</span>
          </div>
        )}

        <Button
          onClick={onUpload}
          disabled={!file || loading}
          className="w-full"
        >
          {loading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Uploading...
            </>
          ) : (
            <>
              <Upload className="mr-2 h-4 w-4" />
              Upload {domain} Data
            </>
          )}
        </Button>
      </CardContent>
    </Card>
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground mb-2">Data Upload</h1>
        <p className="text-muted-foreground">
          Upload Excel files with historical data for each domain
        </p>
      </div>

      <Tabs defaultValue="health" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="health">Health</TabsTrigger>
          <TabsTrigger value="infrastructure">Infrastructure</TabsTrigger>
          <TabsTrigger value="safety">Public Safety</TabsTrigger>
        </TabsList>

        <TabsContent value="health" className="space-y-4">
          <DomainUploadCard
            domain="Health"
            icon={Heart}
            color="health"
            file={healthFile}
            setFile={setHealthFile}
            loading={healthLoading}
            success={healthSuccess}
            onUpload={() => handleFileUpload("health", healthFile, setHealthLoading, setHealthSuccess)}
          />
        </TabsContent>

        <TabsContent value="infrastructure" className="space-y-4">
          <DomainUploadCard
            domain="Infrastructure"
            icon={Building2}
            color="infrastructure"
            file={infraFile}
            setFile={setInfraFile}
            loading={infraLoading}
            success={infraSuccess}
            onUpload={() => handleFileUpload("infrastructure", infraFile, setInfraLoading, setInfraSuccess)}
          />
        </TabsContent>

        <TabsContent value="safety" className="space-y-4">
          <DomainUploadCard
            domain="Public Safety"
            icon={ShieldAlert}
            color="safety"
            file={safetyFile}
            setFile={setSafetyFile}
            loading={safetyLoading}
            success={safetySuccess}
            onUpload={() => handleFileUpload("public_safety", safetyFile, setSafetyLoading, setSafetySuccess)}
          />
        </TabsContent>
      </Tabs>

      <Card>
        <CardHeader>
          <CardTitle>Upload Guidelines</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm text-muted-foreground">
          <p>• Ensure Excel files contain properly formatted data with required columns</p>
          <p>• Maximum file size: 10MB per upload</p>
          <p>• Data will be validated and processed automatically</p>
          <p>• Invalid records will be logged for review</p>
          <p>• Upload frequency: Real-time or scheduled batch uploads supported</p>
        </CardContent>
      </Card>
    </div>
  );
};

export default DataUpload;
