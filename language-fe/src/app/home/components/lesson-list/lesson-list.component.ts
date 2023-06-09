import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { HomeService } from '../../home.service';
import { Lesson } from '../../models/lesson.interface';
import { AuthService } from 'src/app/auth.service';

@Component({
  selector: 'app-lesson-list',
  templateUrl: './lesson-list.component.html',
  styleUrls: ['./lesson-list.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class LessonListComponent implements OnInit {
  lessonList: Lesson[] = [];

  constructor(
    private homeService: HomeService,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    this.authService.isLoggedIn$.subscribe((isLoggedIn) => {
      if (isLoggedIn) {
        this.homeService.getLessonList().subscribe((lessons) => {
          this.homeService.setLessonList(lessons).subscribe((lessonList) => {
            this.lessonList = lessonList;
          });
        });
      }
    });
  }

  deleteLesson(id: any): void {
    this.homeService.deleteLesson(id).subscribe((res) => {
      this.homeService.getLessonList().subscribe((lessons) => {
        this.homeService.setLessonList(lessons).subscribe((lessonList) => {
          this.lessonList = lessonList;
        });
      });
    });
  }
}
