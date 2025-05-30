import { Controller, Get, Post, Param, Body } from '@nestjs/common';
import { UsersService } from './users.service';

@Controller('users')
export class UsersController {
  constructor(private usersService: UsersService) {}

  @Get()
  getUsers() {
    return this.usersService.findAll();
  }
  @Get(":id")
  getUsersById(@Param('id') id: number) {
    return this.usersService.findOne(null, 1);
  }
  @Post(":id")
  updateUser(@Param('id') id: number, @Body() toUpdate: any) {
    return { "status": "ok" }
  }
}
