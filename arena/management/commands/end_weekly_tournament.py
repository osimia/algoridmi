from django.core.management.base import BaseCommand
from arena.models import ArenaRank


class Command(BaseCommand):
    help = 'Завершает недельный турнир: раздает награды и сбрасывает очки'
    
    def handle(self, *args, **options):
        self.stdout.write('🏆 Завершение недельного турнира...')
        
        # Завершаем турнир и получаем список наград
        awards = ArenaRank.end_week_tournament()
        
        if awards:
            self.stdout.write(self.style.SUCCESS('\n📊 Награды за неделю:'))
            self.stdout.write('-' * 50)
            
            current_division = None
            for award in awards:
                if award['division'] != current_division:
                    current_division = award['division']
                    self.stdout.write(f"\n🎯 {current_division}:")
                
                self.stdout.write(
                    f"  #{award['position']} {award['user']} - "
                    f"{award['weekly_score']} очков - {award['award']}"
                )
            
            self.stdout.write('-' * 50)
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✅ Турнир завершен! Выдано {len(awards)} наград.'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️ Нет игроков с очками за эту неделю.')
            )
        
        self.stdout.write('🔄 Недельные очки сброшены. Новая неделя началась!')
