import { SocialAuthService } from '@abacritt/angularx-social-login';
import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { Observable } from 'rxjs';
import { AuthService } from 'src/app/auth.service';
import { HomeService } from '../../home.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class HomeComponent implements OnInit {
  fullName: string = '';
  isLoggedIn: boolean = false;
  tabIndex: number = 0;

  constructor(
    private socialAuthService: SocialAuthService,
    private authService: AuthService,
    private homeService: HomeService
  ) {}

  ngOnInit(): void {
    //on login
    this.socialAuthService.authState.subscribe((user) => {
      this.authService.login(user.idToken).subscribe((user_) => {
        this.fullName = JSON.parse(user_).name;
      });
    });

    // check if logged in
    this.authService.isLoggedIn$.subscribe((isLoggedIn) => {
      this.isLoggedIn = isLoggedIn;
    });

    // on refresh
    this.authService.user.subscribe((user_: any) => {
      this.fullName = JSON.parse(user_).name;
    });

    // check tab index
    this.homeService.tabIndex.subscribe((tabIndex) => {
      this.tabIndex = tabIndex;
    });
  }

  logout(): void {
    this.authService.logout();
    // this is to move tab back to about after logout
    window.location.reload();
  }
}
