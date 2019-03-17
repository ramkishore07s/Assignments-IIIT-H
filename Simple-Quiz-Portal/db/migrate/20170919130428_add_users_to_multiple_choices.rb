class AddUsersToMultipleChoices < ActiveRecord::Migration[5.1]
  def change
    add_reference :multiple_choices, :user, foreign_key: true
  end
end
