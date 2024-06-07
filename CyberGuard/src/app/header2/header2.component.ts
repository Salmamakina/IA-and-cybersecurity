import { Component , OnInit} from '@angular/core';

@Component({
  selector: 'app-header2',
  templateUrl: './header2.component.html',
  styleUrls: ['./header2.component.css']
})
export class Header2Component implements OnInit{
  
  constructor() {}

  ngOnInit(): void {
    // No initialization logic needed here since we're reading from local storage
  }
}
