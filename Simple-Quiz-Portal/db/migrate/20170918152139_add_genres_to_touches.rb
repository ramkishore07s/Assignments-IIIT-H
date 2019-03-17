class AddGenresToTouches < ActiveRecord::Migration[5.1]
  def change
    add_reference :touches, :genre, foreign_key: true
  end
end
