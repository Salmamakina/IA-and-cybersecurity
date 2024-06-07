import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Router } from '@angular/router';
@Component({
  selector: 'app-ddos-detection',
  templateUrl: './ddos-detection.component.html',
  styleUrls: ['./ddos-detection.component.css']
})
export class DdosDetectionComponent implements OnInit {
  @ViewChild('fileInput') fileInput!: ElementRef;
  selectedFile: File | null = null;
  uploadedFileName: string | null = null;

  constructor(private http: HttpClient, private router: Router) { } 

  ngOnInit(): void {
    const analyzeElement = document.getElementById('analyzeButton');
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

  analyzetext(): void {
    const textArea = document.getElementById('data') as HTMLTextAreaElement;
    const textData = textArea.value;

    // Convert the text data to an array of numbers
    const features = textData.split(/\s+/).map(Number);
    const requestData = { features };

    this.http.post<any>('http://127.0.0.1:5000/predict', requestData)
    .subscribe({
      next: (response) => {
        console.log('Prediction response:', response);
        // Check if RandomForest is 0 (benign)
        if (response.RandomForest === 0) {
          alert("The analysis indicates that the activity is harmless and poses no threat.");
        } else {

          this.playAlertSound();
          // Navigate to ddos-alert page if not benign
          this.router.navigate(['/alert-ddos']); // Adjust the path according to your routing configuration
        }
      },
      error: (error: HttpErrorResponse) => {
        console.error('Error occurred during prediction:', error);
        alert('An error occurred during prediction.');
      }
    });
  }

  playAlertSound(): void {
    const audioContext = new (window as any).AudioContext || (window as any)['webkitAudioContext'];
    const audioSource = audioContext.createBufferSource();
    fetch('/assets/alert.mp3')
     .then(response => response.arrayBuffer())
     .then(arrayBuffer => audioContext.decodeAudioData(arrayBuffer))
     .then(audioBuffer => {
        audioSource.buffer = audioBuffer;
        audioSource.connect(audioContext.destination);
        audioSource.start(0); // Start playing immediately
      });
  }

}
