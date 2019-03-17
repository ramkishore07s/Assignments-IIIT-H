class AddUrlToSingleAnswer < ActiveRecord::Migration[5.1]
  def change
    add_column :single_answers, :url, :string
  end
end
