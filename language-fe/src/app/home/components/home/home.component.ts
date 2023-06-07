import { SocialAuthService } from '@abacritt/angularx-social-login';
import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { AuthService } from 'src/app/auth.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class HomeComponent implements OnInit {
  fullName: string = '';
  isLoggedIn: boolean = false;

  constructor(
    private socialAuthService: SocialAuthService,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    //on login
    this.socialAuthService.authState.subscribe((user) => {
      this.authService.login(user.idToken).subscribe((user_) => {
        this.fullName = user_.name;
      });
    });

    // check if logged in
    this.authService.isLoggedIn$.subscribe((isLoggedIn) => {
      this.isLoggedIn = isLoggedIn;
    });

    // on refresh
    this.authService.user.subscribe((user_: any) => {
      this.fullName = user_.name;
    });
  }

  logout(): void {
    this.authService.logout();
    // this is to move tab back to about after logout
    window.location.reload();
  }
}
