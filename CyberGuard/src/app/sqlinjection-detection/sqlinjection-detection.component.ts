import { Component, OnInit , ViewChild, ElementRef} from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-sqlinjection-detection',
  templateUrl: './sqlinjection-detection.component.html',
  styleUrls: ['./sqlinjection-detection.component.css']
})
export class SqlinjectionDetectionComponent implements OnInit{
  @ViewChild('fileInput') fileInput!: ElementRef; 
  selectedFile: File | null = null;
  uploadedFileName: string | null = null;

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    const analyzeElement = document.getElementById('analyzeButton');

    if (analyzeElement) {
      analyzeElement.addEventListener('click', () => {
        window.location.href = '/alert-ddos'; 
      });
    }
  }

  onFileSelected(files: FileList | null): void {
    if (files && files.length > 0) {
      const file = files[0];
      this.selectedFile = file;
      this.uploadedFileName = file.name;
      const fileReader = new FileReader();
      fileReader.onload = (e) => {
        const content = e.target?.result as string;
        if (content) {
          this.fileInput.nativeElement.value = content;
        }
      };
      fileReader.readAsText(file);
    }
  }


  analyzeFile(): void {
    if (this.selectedFile) {
      const formData = new FormData();
      formData.append('file', this.selectedFile);

      this.http.post('/analyze', formData)
        .subscribe({
          next: (response: any) => {
            if (response.ok) {
              console.log('Analysis result:', response.data);
              // Handle the analysis result here
            } else {
              console.error('Failed to analyze file');
            }
          },
          error: (error: HttpErrorResponse) => {
            console.error('Error:', error.message);
          }
        });
    } else {
      console.error('No file selected');
    }
  }
}
