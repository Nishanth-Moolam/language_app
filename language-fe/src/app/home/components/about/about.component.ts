import { Component, ViewEncapsulation } from '@angular/core';
import { HomeService } from '../../home.service';

@Component({
  selector: 'app-about',
  templateUrl: './about.component.html',
  styleUrls: ['./about.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class AboutComponent {
  constructor(private homeService: HomeService) {}

  // ngOnInit(): void {
  //   this.homeService.getLessonList().subscribe((lessons) => {});
  // }
}
