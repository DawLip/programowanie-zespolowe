import { Controller, Get, Param } from '@nestjs/common';
import { AppService } from './app.service';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  getHello(): string { return this.appService.getHello(); }

  @Get('dashboard')
  getDashboard(): any { return this.appService.getDashboard();}

  @Get('aside')
  getAside(): any { return this.appService.getAside(); }

  @Get('search/:query')
  getSearch(@Param() params: any):any { return this.appService.getSearch(params.query); }

  @Get('group/*')
  getGroup():any { return this.appService.getGroup(); }
}
