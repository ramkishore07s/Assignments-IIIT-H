class AddUsersToTouches < ActiveRecord::Migration[5.1]
  def change
    add_reference :touches, :user, foreign_key: true
  end
end
